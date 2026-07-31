from django.contrib import admin

from apps.cadastros.models import Funcao


@admin.register(Funcao)
class FuncaoAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "ativo",
    )

    search_fields = ("nome",)
