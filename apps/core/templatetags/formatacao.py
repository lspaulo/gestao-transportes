from decimal import Decimal

from django import template

register = template.Library()


@register.filter
def moeda_br(valor):
    if valor is None:
        return "R$ 0,00"

    valor = Decimal(str(valor))

    valor_formatado = f"{valor:,.2f}"

    valor_formatado = (
        valor_formatado.replace(",", "X").replace(".", ",").replace("X", ".")
    )

    return f"R$ {valor_formatado}"
