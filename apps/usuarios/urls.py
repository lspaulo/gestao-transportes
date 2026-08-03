from django.urls import path

from .views import (
    meu_perfil,  # type: ignore
    usuario_create,
    usuario_list,  # type: ignore
    usuario_update,  # type: ignore
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
    path(
        "",
        usuario_list,
        name="usuario_list",
    ),
    path(
        "<int:pk>/editar/",
        usuario_update,
        name="usuario_update",
    ),
]
