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

    # ==========================================================
    # DADOS HISTÓRICOS DO ADIANTAMENTO
    # ==========================================================
    #
    # Estes campos armazenam uma fotografia dos dados utilizados
    # no adiantamento.
    #
    # A relação conta_bancaria continua existindo para manter
    # a referência ao cadastro atual, mas o histórico não depende
    # de futuras alterações nesse cadastro.
    #

    historico_nome_motorista = models.CharField(
        "Nome do Motorista",
        max_length=150,
        blank=True,
    )

    historico_cpf_motorista = models.CharField(
        "CPF do Motorista",
        max_length=20,
        blank=True,
    )

    historico_titular = models.CharField(
        "Titular da Conta",
        max_length=150,
        blank=True,
    )

    historico_banco = models.CharField(
        "Banco",
        max_length=100,
        blank=True,
    )

    historico_agencia = models.CharField(
        "Agência",
        max_length=20,
        blank=True,
    )

    historico_digito_agencia = models.CharField(
        "Dígito da Agência",
        max_length=2,
        blank=True,
    )

    historico_numero_conta = models.CharField(
        "Número da Conta",
        max_length=30,
        blank=True,
    )

    historico_digito_conta = models.CharField(
        "Dígito da Conta",
        max_length=2,
        blank=True,
    )

    historico_tipo_conta = models.CharField(
        "Tipo de Conta",
        max_length=20,
        blank=True,
    )

    historico_tipo_chave_pix = models.CharField(
        "Tipo de Chave PIX",
        max_length=20,
        blank=True,
    )

    historico_chave_pix = models.CharField(
        "Chave PIX",
        max_length=150,
        blank=True,
    )

    # ==========================================================
    # DEMAIS DADOS DO ADIANTAMENTO
    # ==========================================================

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

    lote = models.ForeignKey(
        "financeiro.LoteAdiantamento",
        on_delete=models.PROTECT,
        related_name="adiantamentos",
        blank=True,
        null=True,
        verbose_name="Lote",
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

    def _atualizar_historico(self):
        """
        Copia para o adiantamento os dados utilizados
        no momento da criação/edição do registro.
        """

        if not self.funcionario_id or not self.conta_bancaria_id:  # type: ignore[attr-defined]
            return

        funcionario = self.funcionario
        conta = self.conta_bancaria

        self.historico_nome_motorista = funcionario.nome or ""

        self.historico_cpf_motorista = getattr(funcionario, "cpf", "") or ""

        self.historico_titular = conta.titular or ""

        self.historico_banco = conta.get_banco_display() or ""

        self.historico_agencia = conta.agencia or ""

        self.historico_digito_agencia = conta.digito_agencia or ""

        self.historico_numero_conta = conta.numero_conta or ""

        self.historico_digito_conta = conta.digito_conta or ""

        self.historico_tipo_conta = conta.get_tipo_conta_display()

        self.historico_tipo_chave_pix = conta.get_tipo_chave_pix_display()

        self.historico_chave_pix = conta.chave_pix or ""

    def save(self, *args, **kwargs):
        if self.funcionario_id:  # type: ignore[attr-defined]
            self.empresa = self.funcionario.empresa

        if not self.numero:
            self.numero = self.gerar_numero()

        # Enquanto o adiantamento estiver em rascunho,
        # mantém o histórico sincronizado com os cadastros.
        if self.status == StatusAdiantamento.RASCUNHO:
            self._atualizar_historico()

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
