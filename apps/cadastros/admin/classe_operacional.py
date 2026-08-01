from django.contrib import admin

from apps.cadastros.models import ClasseOperacional  # type:ignore


@admin.register(ClasseOperacional)
class ClasseOperacionalAdmin(admin.ModelAdmin):
    list_display = (
        "ordem",
        "nome",
        "possui_placa",
        "ativo",
    )

    list_filter = (
        "ativo",
        "possui_placa",
    )

    search_fields = ("nome",)

    ordering = (
        "ordem",
        "nome",
    )
