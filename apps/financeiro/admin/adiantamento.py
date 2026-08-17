from django.contrib import admin

from apps.financeiro.models import Adiantamento


@admin.register(Adiantamento)
class AdiantamentoAdmin(admin.ModelAdmin):
    list_display = (
        "numero",
        "funcionario",
        "empresa",
        "valor",
        "status",
        "data_solicitacao",
    )

    list_filter = (
        "empresa",
        "status",
        "setor",
    )

    search_fields = (
        "numero",
        "funcionario__nome",
    )

    # autocomplete_fields = (
    #     "funcionario",
    #     "empresa",
    #     "conta_bancaria",
    #     "solicitante",
    #     "setor",
    # )

    readonly_fields = (
        "numero",
        "data_solicitacao",
    )
