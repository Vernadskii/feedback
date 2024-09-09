from django.urls import path

from users.api import router as users_router


urlpatterns = [
    path("", users_router),
]
