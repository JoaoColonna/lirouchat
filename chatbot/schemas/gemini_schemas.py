from ninja import Schema

class GeminiSendMessage(Schema):
    conversa_id: int=None
    message: str

class RespostaMensagem(Schema):
    conversa_id: int
    resposta: str