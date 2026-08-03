from django.urls import path

from .views import usuario_create

app_name = "usuarios"

urlpatterns = [
    path(
        "novo/",
        usuario_create,
        name="usuario_create",
    ),
]
