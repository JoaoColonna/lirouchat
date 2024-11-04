import requests
import os
import google.generativeai as genai

generation_config = {
  "temperature": 1.2,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

class GeminiService:
    def __init__(self, api_key):
        self.api_url = ""
        self.api_key = api_key
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

    def send_message(self, message):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        payload = {
            'message': message
        }
        response = requests.post(self.api_url, headers=headers, json=payload)
        return response.json()

    def process_response(self, response):
        # Lógica para processar a resposta do Gemini
        return response.get('reply')
