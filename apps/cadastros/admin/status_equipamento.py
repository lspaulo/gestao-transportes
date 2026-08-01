from django.contrib import admin

from apps.cadastros.models import StatusEquipamento  # type: ignore


@admin.register(StatusEquipamento)
class StatusEquipamentoAdmin(admin.ModelAdmin):
    list_display = (
        "ordem",
        "nome",
        "permite_utilizacao",
        "ativo",
    )

    list_filter = (
        "permite_utilizacao",
        "ativo",
    )

    search_fields = ("nome",)

    ordering = (
        "ordem",
        "nome",
    )
