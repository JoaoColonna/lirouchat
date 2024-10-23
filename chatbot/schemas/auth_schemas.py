from ninja import Schema
from ninja.security import HttpBearer

class LoginSchema(Schema):
    username: str
    password: str

class ChangePasswordSchema(Schema):
    password: str
    new_password: str

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token