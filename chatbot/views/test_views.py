from ninja import Router
from typing import List
from chatbot.schemas.test_schemas import TesteSchema, TesteCreateSchema, TesteMensagem
from django.shortcuts import get_object_or_404
from chatbot.models import Teste
from chatbot.schemas.utility_schemas import Error
from chatbot.services.gemini_service import GeminiService

router = Router()

@router.get("/tests", response={200: dict, 400: Error}, tags=["test"], summary="List all Test")
def list_testes(request):
    _geminiService = GeminiService()
    conversas = _geminiService.get_all_tests_conversations(request.user)
    return {"conversas": conversas} 

@router.delete("/tests/{teste_id}", tags=["test"], summary="Delete a Test by ID")
def delete_teste(request, teste_id: int):
    teste = get_object_or_404(Teste, id=teste_id)
    teste.delete()
    return {"success": True}

@router.post("/create-test", response=TesteMensagem, tags=["test"], summary="Create a new Test")
def init_test(request, payload: TesteCreateSchema):
    _geminiService = GeminiService()
    response = _geminiService.init_test(request.user, payload.tipo)
    return response

@router.post("/answer-test", response=TesteMensagem, tags=["test"], summary="Answer a Test")
def answer_test(request, payload: TesteMensagem):
    _geminiService = GeminiService()
    response = _geminiService.answer_questions(request.user, payload.conversa_id, payload.resposta)
    return response