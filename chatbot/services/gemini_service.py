from datetime import datetime
import os
import google.generativeai as genai
from chatbot.models import Conversa, Mensagem, Teste, TipoMensagem
from chatbot.schemas.gemini_schemas import RespostaMensagem
from chatbot.schemas.test_schemas import TesteMensagem
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv

load_dotenv()

generation_config = {
  "temperature": 1.0,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv('gemini_api_key')
        self.generation_config = generation_config
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=f"Você é o Lirouchat. Você é um chatbot educacional, com o proposíto de ensinar pessoas, jovens, crianças, adultos e idosos (sempre visando o aprendizado). Você deve responder as perguntas do usuário de acordo com a sua idade. Acima de 18 anos não precisa relevar isso.",
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            }
        )

    def send_message(self, message, user, conversa_id=None):
        is_new = False
        if conversa_id is None or conversa_id != 0:
            history = self.get_conversation(conversa_id)
            chat = self.model.start_chat(history=history)
            response = chat.send_message(message)
        else:
            conversation = Conversa.objects.create(usuario=user, titulo=message, criada_em=datetime.now())
            conversa_id = conversation.id
            if user.age is not None and user.age < 18:
                response = self.model.generate_content(f"Sabendo que o usuário a seguir tem {user.age} anos, responda todas as perguntas a seguir: {message}")
            else:
                response = self.model.generate_content(message)
            is_new = True

        tipo_mensagem = TipoMensagem.objects.get(nome='conversa')

        self.save_message_to_db(message, user, conversa_id, is_user=True, tipo_mensagem=tipo_mensagem)
        self.save_message_to_db(response.text, user, conversa_id, is_user=False, tipo_mensagem=tipo_mensagem)
        
        if is_new:
            self.update_title_conversation(conversa_id, message)

        resposta = RespostaMensagem(conversa_id=conversa_id, resposta=response.text)
        return resposta

    def save_message_to_db(self, message, user, conversa_id, is_user, tipo_mensagem=None):
        conversation = Conversa.objects.get(id=conversa_id)
        Mensagem.objects.create(
            conversa=conversation,
            usuario=user,
            conteudo=message,
            criada_em=datetime.now(),
            is_user=is_user,
            id_tipo_mensagem=tipo_mensagem
        )
    
    def update_title_conversation(self, conversa_id, message):
        title = self.model.generate_content(f"Crie diretamente um titulo sobre isso: '{message}' para entitular uma conversa de chat. Apenas uma, direto ao ponto")
        conversation = Conversa.objects.get(id=conversa_id)
        conversation.titulo = title.text[:40] + '...'
        conversation.save()

    def get_conversation(self, conversa_id):
        try:
            conversation = Conversa.objects.get(id=conversa_id)
            messages = Mensagem.objects.filter(conversa=conversation).order_by('criada_em')
            history = [
                {"role": "user" if msg.is_user else "model", "parts": msg.conteudo}
                for msg in messages
            ]
            return history
        except Conversa.DoesNotExist:
            return None
    
    def get_conversation_infos(self, conversa_id):
        try:
            conversation = Conversa.objects.get(id=conversa_id)
            return {
                "id": conversation.id,
                "usuario": conversation.usuario.id,
                "titulo": conversation.titulo,
                "criada_em": conversation.criada_em
            }
        except Conversa.DoesNotExist:
            return None
    
    def get_conversations(self, user):
        test_conversations = Teste.objects.filter(usuario=user).values_list('conversa_id', flat=True)
        conversations = Conversa.objects.filter(usuario=user).exclude(id__in=test_conversations).order_by('-criada_em')
        return [
            {
                "id": conversation.id,
                "usuario": conversation.usuario.id,
                "titulo": conversation.titulo,
                "criada_em": conversation.criada_em
            }
            for conversation in conversations
        ]
    
    def init_test(self, user, type_test):
        response = self.model.generate_content(f"Olá. Sabendo que o usuário {user.username} tem {user.age} anos, você irá criar um teste a seguir. Crie de 8 a 10 perguntas aleatórias sobre o seguinte assunto: {type_test}. Lembre-se: crie as perguntas de acordo com o nível de conhecimento do usuário de acordo com a idade dele. Após isso, aguarde ele responder a mensagem, e em seguida corrija as respostas, dando um feedback para ele, com notas de 0 a 10. Pode mandar a numeração também em negrito junto da pergunta.")
        conversation = Conversa.objects.create(usuario=user, titulo=f"Teste: {type_test}", criada_em=datetime.now())
        conversa_id = conversation.id
        tipo_mensagem = TipoMensagem.objects.get(nome='teste')
        self.save_message_to_db(response.text, user, conversa_id, is_user=False, tipo_mensagem=tipo_mensagem)
        Teste.objects.create(usuario=user, titulo=type_test, texto=response.text, criado_em=datetime.now(), conversa=conversation)
        return TesteMensagem(conversa_id=conversa_id, resposta=response.text)
    
    def answer_questions(self, user, conversa_id, message):
        conversation = Conversa.objects.get(id=conversa_id)
        messages = Mensagem.objects.filter(conversa=conversation).order_by('criada_em')
        history = [
            {"role": "user" if msg.is_user else "model", "parts": msg.conteudo}
            for msg in messages
        ]
        chat = self.model.start_chat(history=history)
        response = chat.send_message(message)
        self.save_message_to_db(message, user, conversa_id, is_user=True, tipo_mensagem=TipoMensagem.objects.get(nome='teste'))
        self.save_message_to_db(response.text, user, conversa_id, is_user=False, tipo_mensagem=TipoMensagem.objects.get(nome='teste'))
        return RespostaMensagem(conversa_id=conversa_id, resposta=response.text)

    def get_all_tests_conversations(self, user):
        testes = Teste.objects.filter(usuario=user).order_by('-criado_em')
        conversations = Conversa.objects.filter(usuario=user, id__in=[teste.conversa.id for teste in testes]).order_by('-criada_em')
        return [
            {
                "id": conversation.id,
                "usuario": conversation.usuario.id,
                "titulo": conversation.titulo,
                "criada_em": conversation.criada_em
            }
            for conversation in conversations
        ]