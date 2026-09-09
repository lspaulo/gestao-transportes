from datetime import date
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Max

from apps.cadastros.models import BaseModel, Empresa
from apps.usuarios.models import Setor


class LoteAdiantamento(BaseModel):
    numero = models.CharField(
        "Número",
        max_length=20,
        unique=True,
        editable=False,
    )

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.PROTECT,
        verbose_name="Empresa",
    )

    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="Solicitante",
    )
    setor = models.ForeignKey(
        Setor,
        on_delete=models.PROTECT,
        verbose_name="Setor",
        null=True,
        blank=True,
    )

    data_emissao = models.DateTimeField(
        "Data da Emissão",
        auto_now_add=True,
    )
    responsavel_historico = models.CharField(
        max_length=150,
        blank=True,
    )

    setor_historico = models.CharField(
        max_length=100,
        blank=True,
    )
    emitido_por_historico = models.CharField(
        max_length=150,
        blank=True,
    )

    @property
    def quantidade(self):

        return self.adiantamentos.count()  # type: ignore

    @property
    def total(self):

        return sum(
            (adiantamento.valor for adiantamento in self.adiantamentos.all()),  # type: ignore
            Decimal("0.00"),
        )

    @property
    def total_formatado(self):

        valor = f"{self.total:,.2f}"

        return valor.replace(",", "X").replace(".", ",").replace("X", ".")

    class Meta:
        ordering = [
            "-data_emissao",
        ]
        verbose_name = "Lote de Adiantamento"
        verbose_name_plural = "Lotes de Adiantamentos"

    @classmethod
    def gerar_numero(cls):
        ano = date.today().year

        ultimo = cls.objects.filter(
            numero__startswith=f"ADL-{ano}-",
        ).aggregate(
            ultimo=Max("numero"),
        )["ultimo"]

        if ultimo:
            sequencia = int(ultimo.split("-")[-1]) + 1
        else:
            sequencia = 1

        return f"ADL-{ano}-{sequencia:06d}"

    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = self.gerar_numero()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.numero
