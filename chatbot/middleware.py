from django.http import JsonResponse
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

class CORSMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response["Access-Control-Allow-Origin"] = "http://127.0.0.1:3000"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        return response

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        open_endpoints = [
            "/api/docs", 
            "/api/openapi.json",
            "/api/auth/login",
            "/api/auth/logout",
            "/api/auth/bearer-auth-test",
            "/admin/"
        ]

        if any(request.path.startswith(endpoint) for endpoint in open_endpoints):
            return self.get_response(request)
        
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User not authenticated"}, status=401)
        
        return self.get_response(request)