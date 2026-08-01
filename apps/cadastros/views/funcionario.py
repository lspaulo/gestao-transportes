from django.shortcuts import get_object_or_404, redirect, render

from apps.cadastros.forms import FuncionarioForm
from apps.cadastros.models import Funcionario


def funcionario_list(request):
    funcionarios = Funcionario.objects.all().order_by("nome")

    context = {
        "funcionarios": funcionarios,
    }

    return render(
        request,
        "cadastros/funcionario_list.html",
        context,
    )


def funcionario_create(request):

    if request.method == "POST":
        form = FuncionarioForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("cadastros:funcionario_list")

    else:
        form = FuncionarioForm()

    return render(
        request,
        "cadastros/funcionario_form.html",
        {
            "form": form,
        },
    )


def funcionario_update(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)

    if request.method == "POST":
        form = FuncionarioForm(request.POST, instance=funcionario)

        if form.is_valid():
            form.save()
            return redirect("cadastros:funcionario_list")

    else:
        form = FuncionarioForm(instance=funcionario)

    return render(
        request,
        "cadastros/funcionario_form.html",
        {
            "form": form,
            "titulo": "Editar Funcionário",
        },
    )


def funcionario_toggle_status(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)

    funcionario.ativo = not funcionario.ativo
    funcionario.save()

    return redirect("cadastros:funcionario_list")
