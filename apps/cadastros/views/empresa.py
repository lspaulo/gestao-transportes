from django.shortcuts import get_object_or_404, redirect, render

from apps.cadastros.forms import EmpresaForm
from apps.cadastros.models import Empresa


def empresa_list(request):

    pesquisa = request.GET.get("q", "")

    empresas = Empresa.objects.all()

    if pesquisa:
        empresas = empresas.filter(razao_social__icontains=pesquisa)

    empresas = empresas.order_by("razao_social")

    return render(
        request,
        "cadastros/empresa_list.html",
        {
            "empresas": empresas,
        },
    )


def empresa_create(request):

    if request.method == "POST":
        form = EmpresaForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("cadastros:empresa_list")

    else:
        form = EmpresaForm()

    return render(
        request,
        "cadastros/empresa_form.html",
        {
            "form": form,
        },
    )


def empresa_update(request, pk):

    empresa = get_object_or_404(
        Empresa,
        pk=pk,
    )

    if request.method == "POST":
        form = EmpresaForm(
            request.POST,
            instance=empresa,
        )

        if form.is_valid():
            form.save()

            return redirect("cadastros:empresa_list")

    else:
        form = EmpresaForm(
            instance=empresa,
        )

    return render(
        request,
        "cadastros/empresa_form.html",
        {
            "form": form,
        },
    )


def empresa_toggle_status(request, pk):

    empresa = get_object_or_404(
        Empresa,
        pk=pk,
    )

    empresa.ativo = not empresa.ativo

    empresa.save()

    return redirect("cadastros:empresa_list")
