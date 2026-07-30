from django.shortcuts import redirect, render

from .forms import FuncionarioForm
from .models import Funcionario


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
