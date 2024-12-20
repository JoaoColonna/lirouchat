from ninja.security import django_auth
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from ninja import Router
from chatbot.schemas.auth_schemas import LoginSchema, AuthBearer, ChangePasswordSchema
from chatbot.schemas.utility_schemas import Error, Result

router = Router()

@router.get("/set-csrf-token", tags=["auth"])
def set_csrf_token(request):
    return {"csrftoken": get_token(request)}

@router.post("/login", response={200: Result, 400: Error}, description="Login a user", tags=["auth"])
def login_user(request, data: LoginSchema):
    user = authenticate(request, username=data.username, password=data.password)
    if user is None:
        user = authenticate(request, email=data.username, password=data.password)
    
    if user is not None:
        login(request, user)
        return {
            "status": "success",
            "result": "Login successful"
        }
    else:
        return 400, {
            "status": "error",
            "message": "Invalid credentials"
        }

@router.post("/logout", response={200: Result, 400: Error}, description="Logout a user", tags=["auth"],  auth=django_auth)
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return {
                "status": "success",
                "result": "Logout successful"
            }
    else:
        return 400, {
            "status": "error",
            "message": "You are not logged in"
        }
    
@router.post("/change-password", response={200: Result, 400: Error}, description="Change user password", tags=["auth"],  auth=django_auth)
def change_password(request, data: ChangePasswordSchema):
    user = authenticate(request, username=request.user.username, password=data.password)
    if user is not None and request.user.id == user.id:
        user.set_password(data.new_password)
        user.save()
        return {
            "status": "success",
            "result": "Password changed successfully"
        }
    elif data.password == data.new_password:
        return 400, {
            "status": "error",
            "message": "Passwords are the same"
        }
    else:
        return 400, {
            "status": "error",
            "message": "Invalid password"
        }

@router.get("/user", auth=django_auth, tags=["auth"], response={200: dict}, description="Get user information")
def user(request):
    secret_fact = (
        "The moment one gives close attention to any thing, even a blade of grass",
        "it becomes a mysterious, awesome, indescribably magnificent world in itself."
    )
    return {
        "username": request.user.username,
        "email": request.user.email,
        "secret_fact": secret_fact,
        "age" : request.user.age
    }
    
@router.get("/auth-test", tags=["auth"],  auth=django_auth)
def auth_user_test(request):
    return {
        "status": "success", 
        "message": "You have access to this endpoint",
        "data": {
            "user-id": request.user.id,
            "user-name": request.user.username,
            "user-email": request.user.email,
            "user-age": request.user.age
        },
    }

    
@router.get("/bearer-auth-test", auth=AuthBearer(), response={200: Result, 403: Error}, description="Protected endpoint", tags=["auth"])
def protected(request):
    if request.auth:
        return {"message": "You have access to this endpoint"}
    else:
        return 403 , {
            "status": "error",
            "result": "You don't have access to this endpoint"
        }