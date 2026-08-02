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
    @admin.display(description="Setor")
    def setor(self, obj):
        return obj.funcionario.setor

    list_display = (
        "usuario",
        "funcionario",
        "setor",
        "perfil",
    )

    list_filter = ("perfil",)

    search_fields = (
        "usuario__username",
        "funcionario__nome",
    )
