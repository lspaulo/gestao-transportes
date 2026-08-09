from django.contrib import admin

from apps.cadastros.models import Setor


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "ativo",
    )

    list_filter = ("ativo",)

    search_fields = ("nome",)
