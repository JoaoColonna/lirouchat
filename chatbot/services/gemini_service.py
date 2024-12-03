from datetime import datetime
import os
import google.generativeai as genai
from chatbot.models import Conversa, Mensagem
from chatbot.schemas.gemini_schemas import RespostaMensagem
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

        self.save_message_to_db(message, user, conversa_id, is_user=True)
        self.save_message_to_db(response.text, user, conversa_id, is_user=False)
        
        if is_new:
            self.update_title_conversation(conversa_id, message)

        resposta = RespostaMensagem(conversa_id=conversa_id, resposta=response.text)
        return resposta

    def save_message_to_db(self, message, user, conversa_id, is_user):
        conversation = Conversa.objects.get(id=conversa_id)
        Mensagem.objects.create(
            conversa=conversation,
            usuario=user,
            conteudo=message,
            criada_em=datetime.now(),
            is_user=is_user
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
        conversations = Conversa.objects.filter(usuario=user).order_by('-criada_em')
        return [
            {
                "id": conversation.id,
                "usuario": conversation.usuario.id,
                "titulo": conversation.titulo,
                "criada_em": conversation.criada_em
            }
            for conversation in conversations
        ]
    
    def just_send_message(self, message, user, conversa_id=None):
        response = self.model.generate_content("Oá, tudo bem por aí?")
        resposta = RespostaMensagem(conversa_id=0, resposta=response.text)
        return resposta
