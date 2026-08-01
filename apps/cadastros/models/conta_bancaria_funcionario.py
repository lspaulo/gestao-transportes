from django.db import models
from django.db.models import Q

from .base import BaseModel
from .funcionario import Funcionario


class ContaBancariaFuncionario(BaseModel):
    class TipoConta(models.TextChoices):
        CORRENTE = "corrente", "Conta corrente"
        POUPANCA = "poupanca", "Conta poupança"

    class TipoChavePix(models.TextChoices):
        CPF = "cpf", "CPF"
        TELEFONE = "telefone", "Telefone"
        EMAIL = "email", "E-mail"
        ALEATORIA = "aleatoria", "Chave aleatória"

    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.PROTECT,
        related_name="contas_bancarias",
        verbose_name="Funcionário",
    )

    banco = models.CharField(
        max_length=100,
        verbose_name="Banco",
    )

    agencia = models.CharField(
        max_length=20,
        verbose_name="Agência",
    )

    numero_conta = models.CharField(
        max_length=30,
        verbose_name="Número da conta",
    )

    tipo_conta = models.CharField(
        max_length=10,
        choices=TipoConta.choices,
        default=TipoConta.CORRENTE,
        verbose_name="Tipo de conta",
    )

    tipo_chave_pix = models.CharField(
        max_length=10,
        choices=TipoChavePix.choices,
        default=TipoChavePix.CPF,
        verbose_name="Tipo de chave PIX",
    )

    chave_pix = models.CharField(
        max_length=150,
        verbose_name="Chave PIX",
    )

    padrao = models.BooleanField(
        default=True,
        verbose_name="Conta padrão",
    )

    class Meta:
        ordering = ["funcionario__nome", "-padrao", "banco"]
        verbose_name = "Conta bancária de funcionário"
        verbose_name_plural = "Contas bancárias de funcionários"
        constraints = [
            models.UniqueConstraint(
                fields=["funcionario"],
                condition=Q(padrao=True),
                name="uma_conta_padrao_por_funcionario",
            ),
        ]

    def __str__(self):
        return f"{self.funcionario} - {self.banco} ({self.numero_conta})"
