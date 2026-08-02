from django.db import models

from .base import BaseModel


class Empresa(BaseModel):
    razao_social = models.CharField(
        "Razão Social",
        max_length=150,
        unique=True,
    )

    nome_fantasia = models.CharField("Nome Fantasia", max_length=150, blank=True)

    cnpj = models.CharField("CNPJ", max_length=18, unique=True)

    inscricao_estadual = models.CharField(
        "Inscrição Estadual", max_length=20, blank=True
    )

    telefone = models.CharField("Telefone", max_length=20, blank=True)

    email = models.EmailField("Email", blank=True)

    observacao = models.TextField(
        "Observação",
        blank=True,
    )

    def __str__(self):
        return self.nome_fantasia or self.razao_social

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["razao_social"]
