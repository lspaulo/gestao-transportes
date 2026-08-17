from django.db import models


class FinalidadeAdiantamento(models.TextChoices):
    DESPESAS_VIAGEM = (
        "despesas_viagem",
        "Despesas com viagens",
    )

    ALIMENTACAO = (
        "alimentacao",
        "Alimentação",
    )

    HOSPEDAGEM = (
        "hospedagem",
        "Hospedagem",
    )

    PEDAGIO = (
        "pedagio",
        "Pedágio",
    )

    ABASTECIMENTO = (
        "abastecimento",
        "Abastecimento",
    )

    EMERGENCIA = (
        "emergencia",
        "Emergência",
    )

    OUTROS = (
        "outros",
        "Outros",
    )
