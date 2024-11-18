from ninja import Router
from chatbot.schemas.utility_schemas import Error
from chatbot.schemas.gemini_schemas import GeminiSendMessage, RespostaMensagem
from chatbot.services.gemini_service import GeminiService

router = Router()

@router.post("/send-message", response={200: RespostaMensagem, 400: Error}, description="Send a message to the chatbot", tags=["chat"])
def send_message(request, data: GeminiSendMessage):
    if not data.message:
        return 400, {"error": "Message is required"}
    
    _geminiService = GeminiService()
    resposta = _geminiService.send_message(data.message, request.user, data.conversa_id)
    return 200, {
        "conversa_id": resposta.conversa_id,
        "resposta": resposta.resposta
    }   
            

@router.get("/conversation/{conversation_id}", response={200: dict, 400: Error}, description="Get a conversation", tags=["chat"])
def get_conversation(request, conversation_id: int):
    _geminiService = GeminiService()
    conversation = _geminiService.get_conversation(conversation_id)
    if not conversation:
        return 400, {"error": "Conversation not found"}
    
    return {"conversation": conversation}

@router.get("/conversation-infos/{conversation_id}", response={200: dict, 400: Error}, description="Get a conversation title", tags=["chat"])
def get_conversation_title(request, conversation_id: int):
    _geminiService = GeminiService()
    conversa = _geminiService.get_conversation_infos(conversation_id)
    if not conversa:
        return 400, {"error": "Conversation not found"}
    
    return {"conversa": conversa}

@router.get("/conversations", response={200: dict, 400: Error}, description="Get all conversations", tags=["chat"])
def get_conversations(request):
    _geminiService = GeminiService()
    conversas = _geminiService.get_conversations(request.user)
    return {"conversas": conversas}
