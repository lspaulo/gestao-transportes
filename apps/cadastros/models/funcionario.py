from django.db import models

from apps.core.validators.cpf import normalizar_cpf

from .base import BaseModel
from .funcao import Funcao


class Funcionario(BaseModel):
    nome = models.CharField(max_length=200, verbose_name="Nome")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    email = models.EmailField(
        blank=True,
        verbose_name="E-mail",
    )

    telefone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Telefone",
    )
    numero_cnh = models.CharField(
        max_length=30, blank=True, verbose_name="Número da CNH"
    )
    validade_cnh = models.DateField(
        blank=True, null=True, verbose_name="Validade da CNH"
    )
    funcao = models.ForeignKey(
        Funcao, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Função"
    )
    empresa = models.ForeignKey(
        "cadastros.Empresa",
        on_delete=models.PROTECT,
        verbose_name="Empresa",
    )
    cursos = models.TextField(blank=True, verbose_name="Cursos")
    observacao = models.TextField(blank=True, verbose_name="Observações")

    # Novos campos profissionais
    data_admissao = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de admissão",
    )

    matricula = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Matrícula",
    )

    codigo_fornecedor = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Código fornecedor",
    )

    # Endereço residencial
    cep = models.CharField(
        max_length=9,
        blank=True,
        verbose_name="CEP",
    )

    logradouro = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Logradouro",
    )

    numero_endereco = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Número",
    )

    complemento = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Complemento",
    )

    bairro = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Bairro",
    )

    cidade = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Cidade",
    )

    uf = models.CharField(
        max_length=2,
        blank=True,
        verbose_name="UF",
    )

    class Meta:
        ordering = ["nome"]
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        self.cpf = normalizar_cpf(self.cpf)
        super().save(*args, **kwargs)
