from django.urls import path

from apps.cadastros.views.funcionario import (  # type: ignore
    funcionario_create,
    funcionario_list,
    funcionario_update,
)

app_name = "cadastros"

urlpatterns = [
    path(
        "funcionarios/",
        funcionario_list,
        name="funcionario_list",
    ),
    path(
        "funcionarios/novo/",
        funcionario_create,
        name="funcionario_create",
    ),
    path(
        "funcionarios/<int:pk>/editar/",
        funcionario_update,
        name="funcionario_update",
    ),
]
