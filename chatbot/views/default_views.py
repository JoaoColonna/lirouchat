from ninja import Router
from chatbot.schemas.utility_schemas import Error
router = Router()

@router.get("/", response={200: dict, 400: Error}, description="Show the Index", tags=["Default"])
def index(request):
	return {"message": "Welcome to the Index"}
    