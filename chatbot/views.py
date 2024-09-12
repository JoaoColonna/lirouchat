from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'chatbot/index.html')

def login(request):
    return render(request, 'chatbot/login.html')

def chat(request):
    return render(request, 'chatbot/chat.html')