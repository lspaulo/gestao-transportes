from django.db import models


class Banco(models.TextChoices):
    BANCO_DO_BRASIL = "001", "001 - Banco do Brasil"
    CAIXA = "104", "104 - Caixa Econômica Federal"
    BRADESCO = "237", "237 - Bradesco"
    ITAU = "341", "341 - Itaú"
    SANTANDER = "033", "033 - Santander"
    SICREDI = "748", "748 - Sicredi"
    SICOOB = "756", "756 - Sicoob"
    INTER = "077", "077 - Banco Inter"
    NUBANK = "260", "260 - Nubank"
    C6 = "336", "336 - C6 Bank"
    PAGBANK = "290", "290 - PagBank"
    MERCADO_PAGO = "323", "323 - Mercado Pago"
    ORIGINAL = "212", "212 - Banco Original"
    BTG = "208", "208 - BTG Pactual"
