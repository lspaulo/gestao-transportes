from django.urls import path

from .views import (
    meu_perfil,
    usuario_create,
)

app_name = "usuarios"

urlpatterns = [
    path(
        "novo/",
        usuario_create,
        name="usuario_create",
    ),
    path(
        "perfil/",
        meu_perfil,
        name="meu_perfil",
    ),
]
