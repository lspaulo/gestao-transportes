from django.db import models

from .base import BaseModel
from .classe_operacional import ClasseOperacional  # type: ignore
from .empresa import Empresa
from .status_equipamento import StatusEquipamento  # type: ignore


class Equipamento(BaseModel):
    frota = models.CharField(
        "Frota",
        max_length=20,
        unique=True,
    )

    empresa = models.ForeignKey(
        Empresa,
        verbose_name="Empresa",
        on_delete=models.PROTECT,
        related_name="equipamentos",
    )

    classe_operacional = models.ForeignKey(
        ClasseOperacional,
        verbose_name="Classe Operacional",
        on_delete=models.PROTECT,
        related_name="equipamentos",
    )

    status = models.ForeignKey(
        StatusEquipamento,
        verbose_name="Status",
        on_delete=models.PROTECT,
        related_name="equipamentos",
    )

    placa = models.CharField(
        "Placa",
        max_length=10,
        blank=True,
    )

    descricao = models.CharField(
        "Descrição",
        max_length=150,
    )

    marca = models.CharField(
        "Marca",
        max_length=60,
        blank=True,
    )

    modelo = models.CharField(
        "Modelo",
        max_length=60,
        blank=True,
    )

    ano_fabricacao = models.PositiveSmallIntegerField(
        "Ano Fabricação",
        null=True,
        blank=True,
    )

    ano_modelo = models.PositiveSmallIntegerField(
        "Ano Modelo",
        null=True,
        blank=True,
    )

    renavam = models.CharField(
        "Renavam",
        max_length=20,
        blank=True,
    )

    chassi = models.CharField(
        "Chassi",
        max_length=30,
        blank=True,
    )

    cor = models.CharField(
        "Cor",
        max_length=30,
        blank=True,
    )

    observacao = models.TextField(
        "Observação",
        blank=True,
    )

    class Meta:
        verbose_name = "Equipamento"
        verbose_name_plural = "Equipamentos"
        ordering = ("frota",)

    def __str__(self):
        return f"{self.frota} - {self.descricao}"
