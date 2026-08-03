from django.conf import settings
from django.db import models


class Setor(models.Model):
    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nome",
    )

    responsavel = models.ForeignKey(
        "cadastros.Funcionario",
        on_delete=models.PROTECT,
        related_name="setores_responsavel",
        verbose_name="Responsável",
        null=True,
        blank=True,
    )

    responsavel_substituto = models.ForeignKey(
        "cadastros.Funcionario",
        on_delete=models.PROTECT,
        related_name="setores_substituto",
        verbose_name="Responsável Substituto",
        null=True,
        blank=True,
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


class TipoPerfil(models.TextChoices):
    OPERADOR = "OP", "Operador"
    GESTOR = "GE", "Gestor"
    ADMINISTRADOR = "AD", "Administrador"


class PerfilUsuario(models.Model):
    @property
    def is_admin(self):
        return self.perfil == TipoPerfil.ADMINISTRADOR

    @property
    def is_gestor(self):
        return self.perfil == TipoPerfil.GESTOR

    @property
    def is_operador(self):
        return self.perfil == TipoPerfil.OPERADOR

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
        verbose_name="Usuário",
    )

    funcionario = models.OneToOneField(
        "cadastros.Funcionario",
        on_delete=models.PROTECT,
        related_name="perfil_usuario",
        verbose_name="Funcionário",
        null=True,
        blank=True,
    )
    perfil = models.CharField(
        max_length=2,
        choices=TipoPerfil.choices,
        default=TipoPerfil.OPERADOR,
        verbose_name="Perfil",
    )

    class Meta:
        verbose_name = "Perfil de usuário"
        verbose_name_plural = "Perfis de usuários"

    def __str__(self):
        return f"{self.usuario.username} - {self.funcionario.nome}"  # type: ignore
