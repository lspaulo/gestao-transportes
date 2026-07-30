from django.db import models

from .base import BaseModel


class Funcao(BaseModel):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome")

    descricao = models.TextField(blank=True, verbose_name="Descrição")

    class Meta:
        ordering = ["nome"]
        verbose_name = "Função"
        verbose_name_plural = "Funções"

    def __str__(self):
        return self.nome
