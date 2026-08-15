from django.shortcuts import get_object_or_404, redirect, render

from apps.cadastros.forms import EquipamentoForm
from apps.cadastros.models import Equipamento


def equipamento_list(request):

    pesquisa = request.GET.get("q", "")

    equipamentos = Equipamento.objects.all()

    if pesquisa:
        equipamentos = equipamentos.filter(descricao__icontains=pesquisa)

    equipamentos = equipamentos.order_by("frota")

    return render(
        request,
        "cadastros/equipamento_list.html",
        {
            "equipamentos": equipamentos,
        },
    )


def equipamento_create(request):

    if request.method == "POST":
        form = EquipamentoForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("cadastros:equipamento_list")

    else:
        form = EquipamentoForm()

    return render(
        request,
        "cadastros/equipamento_form.html",
        {
            "form": form,
            "titulo": "Novo Equipamento",
            "descricao": "Cadastre um novo equipamento",
            "icone": "bi-truck",
        },
    )


def equipamento_update(request, pk):

    equipamento = get_object_or_404(
        Equipamento,
        pk=pk,
    )

    if request.method == "POST":
        form = EquipamentoForm(
            request.POST,
            instance=equipamento,
        )

        if form.is_valid():
            form.save()

            return redirect("cadastros:equipamento_list")

    else:
        form = EquipamentoForm(
            instance=equipamento,
        )

    return render(
        request,
        "cadastros/equipamento_form.html",
        {
            "form": form,
            "titulo": "Editar Equipamento",
            "descricao": "Edite os dados do equipamento",
            "icone": "bi-truck",
        },
    )


def equipamento_toggle_status(request, pk):

    equipamento = get_object_or_404(
        Equipamento,
        pk=pk,
    )

    equipamento.ativo = not equipamento.ativo

    equipamento.save()

    return redirect("cadastros:equipamento_list")
