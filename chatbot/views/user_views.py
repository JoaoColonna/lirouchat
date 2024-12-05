from ninja import Router
from chatbot.models import CustomUser  # Importar o modelo CustomUser
from chatbot.schemas.user_schemas import UserCreateSchema, UserUpdateSchema, UserSchema
from chatbot.schemas.utility_schemas import Error
router = Router()

@router.post("/create", response={200: UserSchema, 400: Error}, description="Create a new user", tags=["users"])
def create_user(request, data: UserCreateSchema):
    if CustomUser.objects.filter(username=data.username).exists():  # Usar CustomUser
        return 400, {
            "status": "error",
            "message": "Username already exists"
        }
    user = CustomUser.objects.create_user(username=data.username, password=data.password, email=data.email, age=data.age)  # Usar CustomUser
    return user

@router.put("/update", response={200: dict, 404: Error, 403: Error}, description="Update an existing user", tags=["users"])
def update_user(request, data: UserUpdateSchema):
    if request.user.is_authenticated and request.user.id is not None:    
        try:
            user = CustomUser.objects.get(id=request.user.id)  # Usar CustomUser
            user.username = data.username
            user.email = data.email
            user.age = data.age
            user.save()
            return 200, {
                "status": "success",
                "message": "Informações atualizadas com sucesso!",
                "data": {
                    "username": user.username,
                    "email": user.email,
                    "age": user.age
                }
            }
        except CustomUser.DoesNotExist:
            return 404, {
                "status": "error",
                "message": "User not found"
            }


@router.delete("/delete/{user_id}", response={200: dict, 404: Error}, description="Delete a user", tags=["users"])
def delete_user(request, user_id: int):
    try:
        user = CustomUser.objects.get(id=user_id)  # Usar CustomUser
        if user is None:
            return 404, {
                "status": "error",
                "message": "User not found"
            }
        elif not request.user.is_superuser and user.is_superuser == True:
            return 403, {
                "status": "error",
                "message": "You don't have permission to delete this user"
            }
        user.delete()
        return {
            "status": "success",
            "message": "User deleted successfully"
        }
    except CustomUser.DoesNotExist:
        return 404, {
            "status": "error",
            "message": "User not found"
        }
    
@router.get("/list", response={200: list[UserSchema], 403: Error}, description="List all users", tags=["users"])
def list_users(request):
    if request.user.is_superuser:
        users = CustomUser.objects.all()
        return users
    else:
        return 403, {
            "status": "error",
            "message": "You don't have permission to view this list"
        }

@router.get("/get/{user_id}", response={200: UserSchema, 404: Error, 403: Error}, description="Get a user by ID", tags=["users"])
def get_user(request, user_id: int):
    if request.user.id == user_id or request.user.is_superuser:
        try:
            user = CustomUser.objects.get(id=user_id)  # Usar CustomUser
            return user
        except CustomUser.DoesNotExist:
            return 404, {
                "status": "error",
                "message": "User not found"
            }
    else:
        return 403, {
            "status": "error",
            "message": "You don't have permission to view this user"
        }
