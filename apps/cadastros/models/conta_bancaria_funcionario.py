from django.db import models
from django.db.models import Q

from .bancos import Banco
from .base import BaseModel
from .funcionario import Funcionario


class ContaBancariaFuncionario(BaseModel):
    class TipoConta(models.TextChoices):
        CORRENTE = "corrente", "Conta corrente"
        POUPANCA = "poupanca", "Conta poupança"
        PAGAMENTO = "pagamento", "Conta de pagamento"
        DIGITAL = "digital", "Conta digital"
        SALARIO = "salario", "Conta salário"

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
    titular = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Titular da conta",
    )
    banco = models.CharField(
        max_length=3,
        choices=Banco.choices,
        verbose_name="Banco",
    )

    agencia = models.CharField(
        max_length=20,
        verbose_name="Agência",
    )
    digito_agencia = models.CharField(
        max_length=2,
        blank=True,
        verbose_name="Dígito da agência",
    )

    numero_conta = models.CharField(
        max_length=30,
        verbose_name="Número da conta",
    )
    digito_conta = models.CharField(
        max_length=2,
        blank=True,
        verbose_name="Dígito da conta",
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
        default=False,
        verbose_name="Conta padrão",
    )
    observacao = models.TextField(
        blank=True,
        verbose_name="Observação",
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
        return (
            f"{self.get_banco_display()} "  # type: ignore[attr-defined]
            f"- Ag. {self.agencia}"
            f"{('-' + self.digito_agencia) if self.digito_agencia else ''}"
            f" - CC {self.numero_conta}"
            f"{('-' + self.digito_conta) if self.digito_conta else ''}"
        )

    def save(self, *args, **kwargs):
        if not self.titular:
            self.titular = self.funcionario.nome

        if self.padrao:
            ContaBancariaFuncionario.objects.filter(
                funcionario=self.funcionario,
                padrao=True,
            ).exclude(
                pk=self.pk,
            ).update(
                padrao=False,
            )

        super().save(*args, **kwargs)
