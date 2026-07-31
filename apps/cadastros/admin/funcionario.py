from django.contrib import admin

from apps.cadastros.models import Funcionario


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "cpf",
        "funcao",
        "ativo",
    )

    search_fields = (
        "nome",
        "cpf",
    )

    list_filter = (
        "ativo",
        "funcao",
    )

    ordering = ("nome",)
