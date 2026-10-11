import re


def normalizar_cpf(valor):
    """Remove a pontuação do CPF, mantendo somente os dígitos."""
    if valor is None:
        return ""

    return re.sub(r"\D", "", str(valor))


def validar_cpf(valor):
    """Valida o formato e os dígitos verificadores de um CPF."""
    cpf = normalizar_cpf(valor)

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    numeros = [int(digito) for digito in cpf]

    soma = sum(numeros[i] * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    primeiro_digito = 0 if resto == 10 else resto

    if numeros[9] != primeiro_digito:
        return False

    soma = sum(numeros[i] * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    segundo_digito = 0 if resto == 10 else resto

    return numeros[10] == segundo_digito
