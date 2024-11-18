from datetime import datetime
import os
import google.generativeai as genai
from chatbot.models import Conversa, Mensagem
from chatbot.schemas.gemini_schemas import RespostaMensagem
from asgiref.sync import async_to_sync
from dotenv import load_dotenv

load_dotenv()

generation_config = {
  "temperature": 1.2,
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
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def send_message(self, message, user, conversa_id=None):
        is_new = False
        if conversa_id is None or conversa_id != 0:
            history = self.get_conversation(conversa_id)
            chat = self.model.start_chat(history=history)
            response = chat.send_message(message)
        else:
            conversation = Conversa.objects.create(usuario=user, titulo=message, criada_em=datetime.now())
            conversa_id = conversation.id
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
                {"role": "user" if msg.usuario else "model", "parts": msg.conteudo}
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
                "titulo": conversation.titulo
            }
        except Conversa.DoesNotExist:
            return None
    
    def get_conversations(self, user):
        conversations = Conversa.objects.filter(usuario=user)
        return [
            {
                "id": conversation.id,
                "usuario": conversation.usuario.id,
                "titulo": conversation.titulo
            }
            for conversation in conversations
        ]
