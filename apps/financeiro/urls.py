from django.urls import path

from apps.financeiro.views import (
    adiantamento_confirmar,
    adiantamento_create,
    adiantamento_delete,
    adiantamento_list,
    adiantamento_update,
    contas_funcionario,
    lote_adiantamento_detail,
    lote_adiantamento_list,
    visualizar_pdf_adiantamento,
)

app_name = "financeiro"

urlpatterns = [
    path(
        "adiantamentos/",
        adiantamento_list,
        name="adiantamento_list",
    ),
    path(
        "adiantamentos/confirmar/",
        adiantamento_confirmar,
        name="adiantamento_confirmar",
    ),
    path(
        "adiantamentos/novo/",
        adiantamento_create,
        name="adiantamento_create",
    ),
    path(
        "solicitacoes/",
        lote_adiantamento_list,
        name="lote_adiantamento_list",
    ),
    path(
        "solicitacoes/<int:pk>/",
        lote_adiantamento_detail,
        name="lote_adiantamento_detail",
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
    path(
        "lotes/<int:pk>/pdf/",
        visualizar_pdf_adiantamento,
        name="teste_pdf",
    ),
]
