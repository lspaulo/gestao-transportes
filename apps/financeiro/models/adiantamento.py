from datetime import date

from django.conf import settings
from django.db import models
from django.db.models import Max

from apps.cadastros.models import (
    BaseModel,
    ContaBancariaFuncionario,
    Empresa,
    Funcionario,
)
from apps.usuarios.models import Setor

from .finalidade_adiantamento import FinalidadeAdiantamento
from .managers import AdiantamentoManager
from .status_adiantamento import StatusAdiantamento


class Adiantamento(BaseModel):
    objects = AdiantamentoManager()
    numero = models.CharField(
        "Número",
        max_length=20,
        unique=True,
        editable=False,
    )

    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.PROTECT,
        verbose_name="Motorista",
        related_name="adiantamentos",
    )

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.PROTECT,
        verbose_name="Empresa",
        related_name="adiantamentos",
    )

    conta_bancaria = models.ForeignKey(
        ContaBancariaFuncionario,
        on_delete=models.PROTECT,
        verbose_name="Conta Bancária",
        related_name="adiantamentos",
    )

    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="Solicitante",
        related_name="adiantamentos_solicitados",
    )

    setor = models.ForeignKey(
        Setor,
        on_delete=models.PROTECT,
        verbose_name="Setor",
        related_name="adiantamentos",
    )

    valor = models.DecimalField(
        "Valor",
        max_digits=10,
        decimal_places=2,
    )

    finalidade = models.CharField(
        "Finalidade",
        max_length=30,
        choices=FinalidadeAdiantamento.choices,
        default=FinalidadeAdiantamento.DESPESAS_VIAGEM,
    )

    status = models.CharField(
        "Status",
        max_length=20,
        choices=StatusAdiantamento.choices,
        default=StatusAdiantamento.RASCUNHO,
    )

    data_solicitacao = models.DateTimeField(
        "Data da Solicitação",
        auto_now_add=True,
    )
    observacao = models.TextField(
        "Observação",
        blank=True,
    )

    class Meta:
        ordering = [
            "-data_solicitacao",
        ]

    @classmethod
    def gerar_numero(cls):

        ano = date.today().year

        ultimo = cls.objects.filter(
            numero__startswith=f"AD-{ano}-",
        ).aggregate(
            ultimo=Max("numero"),
        )["ultimo"]

        if ultimo:
            sequencia = int(ultimo.split("-")[-1]) + 1
        else:
            sequencia = 1

        return f"AD-{ano}-{sequencia:06d}"

    def save(self, *args, **kwargs):

        if self.funcionario_id:  # type: ignore
            self.empresa = self.funcionario.empresa

        if not self.numero:
            self.numero = self.gerar_numero()

        super().save(*args, **kwargs)

    def pode_editar(self):

        return self.status == StatusAdiantamento.RASCUNHO

    def pode_excluir(self):

        return self.status == StatusAdiantamento.RASCUNHO

    def pode_gerar_pdf(self):

        return self.status == StatusAdiantamento.RASCUNHO

    def pode_cancelar(self):

        return self.status in (
            StatusAdiantamento.RASCUNHO,
            StatusAdiantamento.SOLICITADO,
        )

    def pode_prestar_contas(self):

        return self.status == StatusAdiantamento.SOLICITADO

    def __str__(self):
        return self.numero
