from django.urls import path

from apps.financeiro.views import (
    adiantamento_create,
    adiantamento_delete,
    adiantamento_list,
    adiantamento_update,
    contas_funcionario,
)

app_name = "financeiro"

urlpatterns = [
    path(
        "adiantamentos/",
        adiantamento_list,
        name="adiantamento_list",
    ),
    path(
        "adiantamentos/novo/",
        adiantamento_create,
        name="adiantamento_create",
    ),
    path(
        "api/funcionarios/<int:funcionario_id>/contas/",
        contas_funcionario,
        name="api_contas_funcionario",
    ),
    path(
        "adiantamentos/<int:pk>/editar/",
        adiantamento_update,
        name="adiantamento_update",
    ),
    path(
        "adiantamentos/<int:pk>/excluir/",
        adiantamento_delete,
        name="adiantamento_delete",
    ),
]
