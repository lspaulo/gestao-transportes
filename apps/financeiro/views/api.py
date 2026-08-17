from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from apps.cadastros.models import (
    ContaBancariaFuncionario,
    Funcionario,
)


def contas_funcionario(request, funcionario_id):

    funcionario = get_object_or_404(
        Funcionario,
        pk=funcionario_id,
    )

    contas = ContaBancariaFuncionario.objects.filter(
        funcionario=funcionario,
    ).order_by("-padrao", "banco")

    dados_contas = []

    conta_padrao = None

    for conta in contas:
        if conta.padrao:
            conta_padrao = conta.id  # type: ignore

        dados_contas.append(
            {
                "id": conta.id,  # type: ignore
                "banco": conta.get_banco_display(),  # type: ignore
                "codigo_banco": conta.banco,
                "agencia": conta.agencia,
                "digito_agencia": conta.digito_agencia,
                "numero": conta.numero_conta,
                "digito": conta.digito_conta,
                "pix": conta.chave_pix,
                "tipo_pix": conta.get_tipo_chave_pix_display(),  # type: ignore
                "padrao": conta.padrao,
            }
        )

    return JsonResponse(
        {
            "funcionario": {
                "id": funcionario.id,  # type: ignore
                "nome": funcionario.nome,
            },
            "empresa": {
                "id": funcionario.empresa.id,
                "nome": funcionario.empresa.nome_fantasia,
            },
            "contas": dados_contas,
            "conta_padrao": conta_padrao,
            "possui_conta": bool(dados_contas),
            "quantidade_contas": len(dados_contas),
        }
    )
