from django.db import models

from .base import BaseModel


class Empresa(BaseModel):
    razao_social = models.CharField(max_length=150, verbose_name="Razão Social")

    nome_fantasia = models.CharField(
        max_length=150, blank=True, verbose_name="Nome Fantasia"
    )

    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")

    inscricao_estadual = models.CharField(
        max_length=20, blank=True, verbose_name="Inscrição Estadual"
    )

    telefone = models.CharField(max_length=20, blank=True)

    email = models.EmailField(blank=True)

    def __str__(self):
        return self.nome_fantasia or self.razao_social

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["razao_social"]
