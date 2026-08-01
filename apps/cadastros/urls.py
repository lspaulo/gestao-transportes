from django.urls import path

from apps.cadastros.views.classe_operacional import (
    classe_operacional_create,
    classe_operacional_list,
    classe_operacional_toggle_status,
    classe_operacional_update,
)
from apps.cadastros.views.funcionario import (  # type: ignore
    funcionario_create,
    funcionario_list,
    funcionario_toggle_status,
    funcionario_update,
)

app_name = "cadastros"

urlpatterns = [
    path(
        "classes-operacionais/nova/",
        classe_operacional_create,
        name="classe_operacional_create",
    ),
    path(
        "classes-operacionais/",
        classe_operacional_list,
        name="classe_operacional_list",
    ),
    path(
        "classes-operacionais/<int:pk>/editar/",
        classe_operacional_update,
        name="classe_operacional_update",
    ),
    path(
        "classes-operacionais/<int:pk>/toggle-status/",
        classe_operacional_toggle_status,
        name="classe_operacional_toggle_status",
    ),
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
    path(
        "funcionarios/<int:pk>/toggle-status/",
        funcionario_toggle_status,
        name="funcionario_toggle_status",
    ),
]
