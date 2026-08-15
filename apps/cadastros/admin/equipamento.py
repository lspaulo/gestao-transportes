from django.contrib import admin

from apps.cadastros.models import Equipamento


@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = (
        "frota",
        "placa",
        "descricao",
        "empresa",
        "classe_operacional",
        "status_operacional",
        "ativo",
    )

    search_fields = (
        "frota",
        "placa",
        "descricao",
    )

    list_filter = (
        "empresa",
        "classe_operacional",
        "status_operacional",
        "ativo",
    )

    ordering = ("frota",)
