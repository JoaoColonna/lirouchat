from ninja import NinjaAPI
from chatbot.views.user_views import router as user_router
from chatbot.views.auth_views import router as auth_router
from chatbot.views.default_views import router as default_views
api = NinjaAPI(title="My API", description="This is a sample API using NinjaAPI", version="1.0.0")

api.add_router("/users/", user_router)
api.add_router("/auth/", auth_router)
api.add_router("/", default_views)