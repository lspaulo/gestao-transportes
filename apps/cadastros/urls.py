from django.urls import path

from apps.cadastros.views.classe_operacional import (  # type: ignore
    classe_operacional_create,
    classe_operacional_list,
    classe_operacional_toggle_status,
    classe_operacional_update,
)
from apps.cadastros.views.empresa import (  # type: ignore
    empresa_create,
    empresa_list,
    empresa_toggle_status,
    empresa_update,
)
from apps.cadastros.views.equipamento import (  # type: ignore
    equipamento_create,
    equipamento_list,
    equipamento_toggle_status,
    equipamento_update,
)
from apps.cadastros.views.funcionario import (  # type: ignore
    funcionario_create,
    funcionario_list,
    funcionario_toggle_status,
    funcionario_update,
)

app_name = "cadastros"

urlpatterns = [
    # Classe Operacional
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
    # Funcionário
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
    # Equipamento
    path(
        "equipamentos/",
        equipamento_list,
        name="equipamento_list",
    ),
    path(
        "equipamentos/novo/",
        equipamento_create,
        name="equipamento_create",
    ),
    path(
        "equipamentos/<int:pk>/editar/",
        equipamento_update,
        name="equipamento_update",
    ),
    path(
        "equipamentos/<int:pk>/status/",
        equipamento_toggle_status,
        name="equipamento_toggle_status",
    ),
    # Empresa
    path(
        "empresas/",
        empresa_list,
        name="empresa_list",
    ),
    path(
        "empresas/novo/",
        empresa_create,
        name="empresa_create",
    ),
    path(
        "empresas/<int:pk>/editar/",
        empresa_update,
        name="empresa_update",
    ),
    path(
        "empresas/<int:pk>/status/",
        empresa_toggle_status,
        name="empresa_toggle_status",
    ),
]
