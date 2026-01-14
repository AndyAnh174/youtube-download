from django.urls import path
from ninja import NinjaAPI

api = NinjaAPI()

from . import views

# Register controllers
api.add_router("/download", views.router)

urlpatterns = [
    path("api/", api.urls),
]
