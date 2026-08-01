from django.conf import settings
from django.db import models


class Setor(models.Model):
    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nome",
    )

    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo",
    )

    class Meta:
        ordering = ["nome"]
        verbose_name = "Setor"
        verbose_name_plural = "Setores"

    def __str__(self):
        return self.nome


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
        verbose_name="Usuário",
    )

    setor = models.ForeignKey(
        Setor,
        on_delete=models.PROTECT,
        related_name="usuarios",
        verbose_name="Setor",
    )

    class Meta:
        verbose_name = "Perfil de usuário"
        verbose_name_plural = "Perfis de usuários"

    def __str__(self):
        return f"{self.usuario.get_full_name() or self.usuario.username} - {self.setor}"
