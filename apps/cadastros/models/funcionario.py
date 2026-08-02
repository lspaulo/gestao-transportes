from django.db import models

from .base import BaseModel
from .funcao import Funcao


class Funcionario(BaseModel):
    nome = models.CharField(max_length=200, verbose_name="Nome")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    numero_cnh = models.CharField(
        max_length=30, blank=True, verbose_name="Número da CNH"
    )
    validade_cnh = models.DateField(
        blank=True, null=True, verbose_name="Validade da CNH"
    )
    funcao = models.ForeignKey(Funcao, on_delete=models.PROTECT, verbose_name="Função")
    setor = models.ForeignKey(
        "usuarios.Setor",
        on_delete=models.PROTECT,
        related_name="funcionarios",
        verbose_name="Setor",
        null=True,
        blank=True,
    )
    cursos = models.TextField(blank=True, verbose_name="Cursos")
    observacao = models.TextField(blank=True, verbose_name="Observações")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

    def __str__(self):
        return self.nome
