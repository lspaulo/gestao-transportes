import logging

from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render

from apps.cadastros.services.importacao_equipamentos import (
    analisar_arquivo,
    executar_importacao,
)
from apps.cadastros.services.modelo_equipamentos import (
    gerar_modelo_equipamentos,
)

logger = logging.getLogger(__name__)

CHAVE_SESSAO = "importacao_equipamentos"


def equipamento_importar(request):
    """Exibe a tela e analisa o arquivo enviado."""

    if request.method == "POST":
        arquivo = request.FILES.get("arquivo")

        if not arquivo:
            messages.error(
                request,
                "Selecione uma planilha Excel para continuar.",
            )
            return redirect("cadastros:equipamento_importar")

        if not arquivo.name.lower().endswith(".xlsx"):
            messages.error(
                request,
                "Envie um arquivo Excel no formato .xlsx.",
            )
            return redirect("cadastros:equipamento_importar")

        try:
            dados = analisar_arquivo(arquivo)

            if not dados["registros"]:
                messages.warning(
                    request,
                    "A planilha não contém equipamentos para importar.",
                )
                return redirect("cadastros:equipamento_importar")

            request.session[CHAVE_SESSAO] = dados
            request.session.modified = True

            return redirect("cadastros:equipamento_importar_preview")

        except Exception as erro:
            logger.exception("Erro ao analisar planilha de equipamentos.")
            messages.error(
                request,
                f"Não foi possível analisar a planilha: {erro}",
            )
            return redirect("cadastros:equipamento_importar")

    return render(
        request,
        "cadastros/equipamento_importar.html",
    )


def equipamento_importar_preview(request):
    """Exibe os registros analisados antes da confirmação."""

    dados = request.session.get(CHAVE_SESSAO)

    if not dados:
        messages.warning(
            request,
            "Envie uma planilha antes de acessar a prévia.",
        )
        return redirect("cadastros:equipamento_importar")

    return render(
        request,
        "cadastros/equipamento_importar_preview.html",
        {"dados": dados},
    )


def equipamento_importar_confirmar(request):
    """Confirma e grava os equipamentos no banco."""

    if request.method != "POST":
        return redirect("cadastros:equipamento_importar")

    dados = request.session.get(CHAVE_SESSAO)

    if not dados:
        messages.error(
            request,
            "A sessão de importação expirou. Envie a planilha novamente.",
        )
        return redirect("cadastros:equipamento_importar")

    # Impede a confirmação enquanto houver registros com erros.
    invalidos = [registro for registro in dados["registros"] if registro["erros"]]

    if invalidos:
        messages.error(
            request,
            "Corrija os erros indicados na planilha e envie o arquivo novamente.",
        )
        return redirect("cadastros:equipamento_importar_preview")

    try:
        quantidade = executar_importacao(dados)

        del request.session[CHAVE_SESSAO]

        messages.success(
            request,
            f"Importação concluída! {quantidade} equipamento(s) cadastrado(s).",
        )

        return redirect("cadastros:equipamento_list")

    except IntegrityError:
        logger.exception("Conflito de integridade na importação de equipamentos.")
        messages.error(
            request,
            "Não foi possível concluir a importação. "
            "Verifique se alguma frota foi cadastrada por outro usuário "
            "durante o processo e envie a planilha novamente.",
        )
        return redirect("cadastros:equipamento_importar_preview")

    except Exception:
        logger.exception("Erro ao confirmar importação de equipamentos.")
        messages.error(
            request,
            "Ocorreu um erro ao importar os equipamentos. "
            "Nenhuma alteração parcial deve ser mantida. "
            "Consulte os logs para identificar a causa.",
        )
        return redirect("cadastros:equipamento_importar_preview")


def equipamento_baixar_modelo(request):
    """Disponibiliza o modelo Excel para download."""

    arquivo = gerar_modelo_equipamentos()

    response = HttpResponse(
        arquivo.getvalue(),
        content_type=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
    )

    response["Content-Disposition"] = (
        'attachment; filename="modelo_importacao_equipamentos.xlsx"'
    )

    return response
