from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from apps.cadastros.forms import FuncionarioForm  # type: ignore
from apps.cadastros.models import Funcionario


def funcionario_list(request):
    pesquisa = request.GET.get("q", "")
    status = request.GET.get("status", "ativos")

    funcionarios = Funcionario.objects.all()

    if status == "ativos":
        funcionarios = funcionarios.filter(ativo=True)

    elif status == "inativos":
        funcionarios = funcionarios.filter(ativo=False)

    if pesquisa:
        funcionarios = funcionarios.filter(nome__icontains=pesquisa)

    funcionarios = funcionarios.order_by("nome")

    paginator = Paginator(funcionarios, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "status": status,
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
            "titulo": "Novo Funcionário",
            "descricao": "Cadastre um novo funcionário",
            "icone": "bi-people",
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
            "descricao": "Edite os dados do funcionário",
            "icone": "bi-people",
        },
    )


def funcionario_toggle_status(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)

    funcionario.ativo = not funcionario.ativo
    funcionario.save()

    return redirect("cadastros:funcionario_list")
