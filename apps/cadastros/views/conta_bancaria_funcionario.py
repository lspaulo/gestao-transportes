from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from apps.cadastros.forms import ContaBancariaFuncionarioForm
from apps.cadastros.models import (
    ContaBancariaFuncionario,
    Funcionario,
)


@login_required
def conta_bancaria_funcionario_list(
    request,
    funcionario_id,
):
    funcionario = get_object_or_404(
        Funcionario,
        pk=funcionario_id,
    )

    contas = ContaBancariaFuncionario.objects.filter(
        funcionario=funcionario,
    ).order_by(
        "-padrao",
        "banco",
    )

    return render(
        request,
        "cadastros/conta_bancaria_funcionario_list.html",
        {
            "funcionario": funcionario,
            "contas": contas,
            "titulo": "Contas Bancárias",
            "descricao": f"Contas cadastradas para {funcionario.nome}.",
            "icone": "bi-bank",
        },
    )


@login_required
def conta_bancaria_funcionario_create(
    request,
    funcionario_id,
):
    funcionario = get_object_or_404(
        Funcionario,
        pk=funcionario_id,
    )

    if request.method == "POST":
        form = ContaBancariaFuncionarioForm(
            request.POST,
            funcionario=funcionario,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Conta bancária cadastrada com sucesso.",
            )

            return redirect(
                "cadastros:conta_bancaria_funcionario_list",
                funcionario.id,  # type: ignore
            )

    else:
        form = ContaBancariaFuncionarioForm(
            funcionario=funcionario,
        )

    return render(
        request,
        "cadastros/conta_bancaria_funcionario_form.html",
        {
            "form": form,
            "funcionario": funcionario,
            "titulo": "Nova Conta Bancária",
            "descricao": "Cadastre uma conta bancária.",
            "icone": "bi-bank",
            "url_cancelar": reverse(
                "cadastros:conta_bancaria_funcionario_list",
                args=[funcionario.id],  # type: ignore
            ),
        },
    )


@login_required
def conta_bancaria_funcionario_update(
    request,
    pk,
):
    conta = get_object_or_404(
        ContaBancariaFuncionario,
        pk=pk,
    )

    if request.method == "POST":
        form = ContaBancariaFuncionarioForm(
            request.POST,
            instance=conta,
            funcionario=conta.funcionario,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Conta atualizada com sucesso.",
            )

            return redirect(
                "cadastros:conta_bancaria_funcionario_list",
                conta.funcionario.id,  # type: ignore
            )

    else:
        form = ContaBancariaFuncionarioForm(
            instance=conta,
            funcionario=conta.funcionario,
        )

    return render(
        request,
        "cadastros/conta_bancaria_funcionario_form.html",
        {
            "form": form,
            "funcionario": conta.funcionario,
            "titulo": "Editar Conta Bancária",
            "descricao": "Atualize os dados da conta.",
            "icone": "bi-bank",
            "url_cancelar": reverse(
                "cadastros:conta_bancaria_funcionario_list",
                args=[conta.funcionario.id],  # type: ignore
            ),
        },
    )


@login_required
def conta_bancaria_funcionario_delete(
    request,
    pk,
):
    conta = get_object_or_404(
        ContaBancariaFuncionario,
        pk=pk,
    )

    funcionario = conta.funcionario

    if request.method == "POST":
        try:
            conta.delete()

            messages.success(
                request,
                "Conta bancária excluída.",
            )

        except ProtectedError:
            messages.error(
                request,
                "Esta conta está sendo utilizada e não pode ser excluída.",
            )

        return redirect(
            "cadastros:conta_bancaria_funcionario_list",
            funcionario.id,  # type: ignore
        )

    return render(
        request,
        "components/confirm_delete.html",
        {
            "objeto": conta,
            "titulo": "Excluir Conta Bancária",
            "url_cancelar": reverse(
                "cadastros:conta_bancaria_funcionario_list",
                args=[funcionario.id],  # type: ignore
            ),
        },
    )
