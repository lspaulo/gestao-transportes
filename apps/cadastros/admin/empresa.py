from django.contrib import admin

from apps.cadastros.models import Empresa


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = (
        "razao_social",
        "nome_fantasia",
        "cnpj",
        "telefone",
        "ativo",
    )

    search_fields = (
        "razao_social",
        "nome_fantasia",
        "cnpj",
    )

    list_filter = ("ativo",)

    ordering = ("razao_social",)
