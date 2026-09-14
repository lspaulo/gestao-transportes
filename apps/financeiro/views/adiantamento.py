from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from apps.financeiro.forms import AdiantamentoForm
from apps.financeiro.models import LoteAdiantamento, StatusAdiantamento
from apps.financeiro.services import AdiantamentoService
from apps.financeiro.services.email_service import EmailService
from apps.financeiro.services.pdf_service import PdfService


@login_required
def teste_pdf(request, pk):

    lote = get_object_or_404(
        LoteAdiantamento,
        pk=pk,
    )

    pdf = PdfService.gerar(lote)

    return FileResponse(
        pdf,
        as_attachment=False,
        filename=f"{lote.numero}.pdf",
    )


@login_required
def adiantamento_create(request):

    if request.method == "POST":
        form = AdiantamentoForm(
            request.POST,
            usuario=request.user,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Adiantamento solicitado com sucesso.",
            )

            return redirect(
                "financeiro:adiantamento_list",
            )

    else:
        form = AdiantamentoForm(
            usuario=request.user,
        )

    return render(
        request,
        "financeiro/adiantamento_form.html",
        {
            "form": form,
            "titulo": "Novo Adiantamento",
            "descricao": "Solicite um novo adiantamento de viagem.",
            "icone": "bi-cash-stack",
        },
    )


from apps.financeiro.models import Adiantamento


@login_required
@login_required
def adiantamento_list(request):

    if request.method == "POST":
        ids = request.POST.getlist(
            "adiantamentos",
        )

        lotes = AdiantamentoService.emitir_lotes(
            request.user,
            ids,
        )

        if not lotes:
            messages.warning(
                request,
                "Nenhum adiantamento disponível para emissão.",
            )

            return redirect(
                "financeiro:adiantamento_list",
            )

        try:
            EmailService.enviar_lotes(lotes)

            messages.success(
                request,
                (
                    f"{len(lotes)} lote(s) criado(s) e "
                    "enviado(s) por e-mail com sucesso."
                ),
            )

        except Exception as erro:
            messages.warning(
                request,
                (
                    f"{len(lotes)} lote(s) criado(s), porém "
                    f"não foi possível enviar o e-mail: {erro}"
                ),
            )

        return redirect(
            "financeiro:adiantamento_list",
        )

    adiantamentos = Adiantamento.objects.visiveis_para(request.user).filter(  # type: ignore
        status=StatusAdiantamento.RASCUNHO,
    )

    return render(
        request,
        "financeiro/adiantamento_list.html",
        {
            "adiantamentos": adiantamentos,
            "titulo": "Adiantamentos",
            "descricao": "Controle de solicitações de adiantamentos.",
            "icone": "bi-cash-stack",
        },
    )


@login_required
def adiantamento_update(
    request,
    pk,
):

    adiantamento = get_object_or_404(
        Adiantamento,
        pk=pk,
    )
    if not adiantamento.pode_editar():
        messages.error(
            request,
            "Este adiantamento não pode mais ser editado.",
        )

        return redirect(
            "financeiro:adiantamento_list",
        )

    if request.method == "POST":
        form = AdiantamentoForm(
            request.POST,
            instance=adiantamento,
            usuario=request.user,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Adiantamento atualizado com sucesso.",
            )

            return redirect(
                "financeiro:adiantamento_list",
            )

    else:
        form = AdiantamentoForm(
            instance=adiantamento,
            usuario=request.user,
        )

    return render(
        request,
        "financeiro/adiantamento_form.html",
        {
            "form": form,
            "titulo": "Editar Adiantamento",
            "descricao": "Atualize os dados do adiantamento.",
            "icone": "bi-cash-stack",
        },
    )


@login_required
def adiantamento_delete(
    request,
    pk,
):

    adiantamento = get_object_or_404(
        Adiantamento,
        pk=pk,
    )
    if not adiantamento.pode_excluir():
        messages.error(
            request,
            "Este adiantamento não pode ser excluído.",
        )

        return redirect(
            "financeiro:adiantamento_list",
        )

    if request.method == "POST":
        adiantamento.delete()

        messages.success(
            request,
            "Adiantamento excluído com sucesso.",
        )

        return redirect(
            "financeiro:adiantamento_list",
        )

    return render(
        request,
        "components/confirm_delete.html",
        {
            "objeto": adiantamento,
            "titulo": "Excluir Adiantamento",
            "url_cancelar": reverse(
                "financeiro:adiantamento_list",
            ),
        },
    )
