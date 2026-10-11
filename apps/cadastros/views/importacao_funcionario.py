import logging

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

logger = logging.getLogger(__name__)

from apps.cadastros.services.importacao_funcionarios import (
    ImportacaoFuncionarioError,
    analisar_arquivo,
    executar_importacao,
)
from apps.cadastros.services.modelo_funcionarios import (
    criar_modelo_funcionarios,
)


def funcionario_importar(request):
    if request.method == "POST":
        arquivo = request.FILES.get("arquivo")

        if not arquivo:
            messages.error(
                request,
                "Selecione um arquivo Excel.",
            )

            return redirect("cadastros:funcionario_importar")

        if not arquivo.name.lower().endswith((".xlsx", ".xlsm")):
            messages.error(
                request,
                "O arquivo deve estar no formato Excel (.xlsx).",
            )

            return redirect("cadastros:funcionario_importar")

        try:
            dados = analisar_arquivo(arquivo)

        except ImportacaoFuncionarioError as exc:
            messages.error(request, str(exc))

            return redirect("cadastros:funcionario_importar")

        request.session["importacao_funcionarios"] = dados

        return render(
            request,
            "cadastros/funcionario_importar_preview.html",
            {
                "dados": dados,
            },
        )

    return render(
        request,
        "cadastros/funcionario_importar.html",
    )


def funcionario_importar_confirmar(request):
    if request.method != "POST":
        return redirect("cadastros:funcionario_importar")

    dados = request.session.get("importacao_funcionarios")

    if not dados:
        messages.error(
            request,
            "Não existe uma importação pendente.",
        )

        return redirect("cadastros:funcionario_importar")

    resumo = dados["resumo"]

    if resumo["funcionarios_com_erro"] > 0 or resumo["contas_com_erro"] > 0:
        messages.error(
            request,
            "Corrija os erros apresentados antes de confirmar a importação.",
        )

        return redirect("cadastros:funcionario_importar")

    try:
        resultado = executar_importacao(dados)

    except Exception:
        logger.exception("Erro durante a importação em massa de funcionários.")

        messages.error(
            request,
            "Não foi possível concluir a importação. "
            "Nenhum registro desta operação foi mantido.",
        )

        return redirect("cadastros:funcionario_importar")

    del request.session["importacao_funcionarios"]

    messages.success(
        request,
        (
            f"{resultado['funcionarios_criados']} "
            "funcionário(s) cadastrado(s) e "
            f"{resultado['contas_criadas']} "
            "conta(s) bancária(s) cadastrada(s)."
        ),
    )

    return redirect("cadastros:funcionario_list")


def funcionario_baixar_modelo(request):
    arquivo = criar_modelo_funcionarios()

    response = HttpResponse(
        arquivo.getvalue(),
        content_type=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
    )

    response["Content-Disposition"] = 'attachment; filename="modelo_funcionarios.xlsx"'

    return response
