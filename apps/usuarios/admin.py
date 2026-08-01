from django.contrib import admin

from .models import PerfilUsuario, Setor


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "ativo",
    )

    list_filter = ("ativo",)

    search_fields = ("nome",)


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "usuario",
        "setor",
    )

    list_filter = ("setor",)

    search_fields = (
        "usuario__username",
        "usuario__first_name",
        "usuario__last_name",
        "usuario__email",
    )
