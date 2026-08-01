from django.db import models

from .base import BaseModel


class StatusEquipamento(BaseModel):
    nome = models.CharField(
        "Nome",
        max_length=50,
        unique=True,
    )

    descricao = models.TextField(
        "Descrição",
        blank=True,
    )

    permite_utilizacao = models.BooleanField(
        "Permite utilização",
        default=True,
    )

    ordem = models.PositiveSmallIntegerField(
        "Ordem",
        default=0,
    )

    class Meta:
        verbose_name = "Status do Equipamento"
        verbose_name_plural = "Status dos Equipamentos"
        ordering = ["ordem", "nome"]

    def __str__(self):
        return self.nome
