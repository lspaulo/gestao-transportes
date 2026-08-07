from django.urls import path

from .views import (
    alterar_senha,  # type: ignore
    meu_perfil,  # type: ignore
    redefinir_senha,  # type: ignore
    usuario_create,
    usuario_list,  # type: ignore
    usuario_toggle_status,  # type: ignore
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
    path(
        "alterar-senha/",
        alterar_senha,
        name="alterar_senha",
    ),
    path(
        "<int:pk>/redefinir-senha/",
        redefinir_senha,
        name="redefinir_senha",
    ),
    path(
        "<int:pk>/status/",
        usuario_toggle_status,
        name="usuario_toggle_status",
    ),
]
