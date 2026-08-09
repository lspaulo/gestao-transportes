from django.db import models


class Setor(models.Model):
    nome = models.CharField(
        "Nome",
        max_length=100,
        unique=True,
    )

    ativo = models.BooleanField(
        "Ativo",
        default=True,
    )

    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"
        ordering = ("nome",)

    def __str__(self):
        return self.nome
