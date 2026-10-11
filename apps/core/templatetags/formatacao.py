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


def somente_digitos(valor):
    """Retorna somente os dígitos de um valor."""
    if valor is None:
        return ""

    return "".join(caractere for caractere in str(valor) if caractere.isdigit())


@register.filter
def cpf_br(valor):
    """Formata CPF como 000.000.000-00."""
    digitos = somente_digitos(valor)

    if len(digitos) != 11:
        return valor or ""

    return f"{digitos[:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:]}"


@register.filter
def cnpj_br(valor):
    """Formata CNPJ como 00.000.000/0000-00."""
    digitos = somente_digitos(valor)

    if len(digitos) != 14:
        return valor or ""

    return f"{digitos[:2]}.{digitos[2:5]}.{digitos[5:8]}/{digitos[8:12]}-{digitos[12:]}"


@register.filter
def telefone_br(valor):
    """Formata telefones brasileiros com DDD."""
    digitos = somente_digitos(valor)

    if len(digitos) == 11:
        return f"({digitos[:2]}) {digitos[2:7]}-{digitos[7:]}"

    if len(digitos) == 10:
        return f"({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}"

    return valor or ""
