from django.contrib import admin

from .models import Funcao, Funcionario  # type: ignore


@admin.register(Funcao)
class FuncaoAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "ativo",
    )

    search_fields = ("nome",)


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
