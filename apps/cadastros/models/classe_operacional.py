from django.db import models

from .base import BaseModel


class ClasseOperacional(BaseModel):
    nome = models.CharField(
        "Nome",
        max_length=100,
        unique=True,
    )

    descricao = models.TextField(
        "Descrição",
        blank=True,
    )

    possui_placa = models.BooleanField(
        "Possui placa",
        default=True,
    )

    ordem = models.PositiveSmallIntegerField(
        "Ordem",
        default=0,
    )

    class Meta:
        verbose_name = "Classe Operacional"
        verbose_name_plural = "Classes Operacionais"
        ordering = ["ordem", "nome"]

    def __str__(self):
        return self.nome
