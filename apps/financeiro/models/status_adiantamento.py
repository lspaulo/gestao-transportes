from django.db import models


class StatusAdiantamento(models.TextChoices):
    RASCUNHO = "rascunho", "Rascunho"
    SOLICITADO = "solicitado", "Solicitado"
    PRESTADO = "prestado", "Prestado"
    CANCELADO = "cancelado", "Cancelado"
