from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from apps.cadastros.forms import FuncaoForm

from ..models import Funcao


@login_required
def funcao_list(request):
    funcoes = Funcao.objects.all()

    return render(
        request,
        "cadastros/funcao_list.html",
        {"funcoes": funcoes},
    )


@login_required
def funcao_create(request):
    if request.method == "POST":
        form = FuncaoForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Função cadastrada com sucesso.",
            )

            return redirect("cadastros:funcao_list")

    else:
        form = FuncaoForm()

    return render(
        request,
        "cadastros/funcao_form.html",
        {
            "form": form,
            "titulo": "Nova Função",
            "descricao": "Cadastre uma nova função.",
            "icone": "bi-person-badge",
        },
    )


@login_required
def funcao_update(request, pk):
    funcao = get_object_or_404(Funcao, pk=pk)

    if request.method == "POST":
        form = FuncaoForm(request.POST, instance=funcao)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Função atualizada com sucesso.",
            )

            return redirect("cadastros:funcao_list")

    else:
        form = FuncaoForm(instance=funcao)

    return render(
        request,
        "cadastros/funcao_form.html",
        {
            "form": form,
            "titulo": "Editar Função",
            "descricao": "Atualize os dados da função.",
            "icone": "bi-person-badge",
        },
    )


@login_required
def funcao_delete(request, pk):
    funcao = get_object_or_404(Funcao, pk=pk)

    if request.method == "POST":
        try:
            funcao.delete()

            messages.success(
                request,
                "Função excluída com sucesso.",
            )

        except ProtectedError:
            messages.error(
                request,
                "Não é possível excluir esta função porque "
                "ela está vinculada a um funcionário.",
            )

        return redirect("cadastros:funcao_list")

    return render(
        request,
        "cadastros/funcao_form.html",
        {
            "form": FuncaoForm(instance=funcao),
            "titulo": "Excluir Função",
            "descricao": "Confirme a exclusão da função.",
            "icone": "bi-trash",
            "excluir": True,
            "funcao": funcao,
        },
    )
