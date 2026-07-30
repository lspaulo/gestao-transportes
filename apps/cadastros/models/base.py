from django.db import models


class BaseModel(models.Model):
    """
    Classe base para todos os modelos do sistema.
    """

    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        abstract = True
