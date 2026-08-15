from django.urls import path

from apps.cadastros.views.classe_operacional import (  # type: ignore
    classe_operacional_create,
    classe_operacional_list,
    classe_operacional_toggle_status,
    classe_operacional_update,
)
from apps.cadastros.views.conta_bancaria_funcionario import (
    conta_bancaria_funcionario_create,
    conta_bancaria_funcionario_delete,
    conta_bancaria_funcionario_list,
    conta_bancaria_funcionario_update,
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

from .views.funcao import (
    funcao_create,
    funcao_delete,
    funcao_list,
    funcao_update,
)
from .views.status_operacional import (
    status_operacional_create,
    status_operacional_list,
    status_operacional_toggle_status,
    status_operacional_update,
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
    # Conta bancária
    path(
        "funcionarios/<int:funcionario_id>/contas-bancarias/",
        conta_bancaria_funcionario_list,
        name="conta_bancaria_funcionario_list",
    ),
    path(
        "funcionarios/<int:funcionario_id>/contas-bancarias/nova/",
        conta_bancaria_funcionario_create,
        name="conta_bancaria_funcionario_create",
    ),
    path(
        "contas-bancarias/<int:pk>/editar/",
        conta_bancaria_funcionario_update,
        name="conta_bancaria_funcionario_update",
    ),
    path(
        "contas-bancarias/<int:pk>/excluir/",
        conta_bancaria_funcionario_delete,
        name="conta_bancaria_funcionario_delete",
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
    # Função
    path(
        "funcoes/",
        funcao_list,
        name="funcao_list",
    ),
    path(
        "funcoes/nova/",
        funcao_create,
        name="funcao_create",
    ),
    path(
        "funcoes/<int:pk>/editar/",
        funcao_update,
        name="funcao_update",
    ),
    path(
        "funcoes/<int:pk>/excluir/",
        funcao_delete,
        name="funcao_delete",
    ),
    # Status Equipamento
    path(
        "status-operacionais/",
        status_operacional_list,
        name="status_operacional_list",
    ),
    path(
        "status-operacionais/novo/",
        status_operacional_create,
        name="status_operacional_create",
    ),
    path(
        "status-operacionais/<int:pk>/editar/",
        status_operacional_update,
        name="status_operacional_update",
    ),
    path(
        "status-operacionais/<int:pk>/alternar-status/",
        status_operacional_toggle_status,
        name="status_operacional_toggle_status",
    ),
]
