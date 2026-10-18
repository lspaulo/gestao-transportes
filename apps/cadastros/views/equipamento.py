from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.cadastros.forms import EquipamentoForm
from apps.cadastros.models import Equipamento


def equipamento_list(request):
    pesquisa = request.GET.get("q", "").strip()
    status = request.GET.get("status", "ativos")

    equipamentos = Equipamento.objects.all()

    # Filtro de status
    if status == "inativos":
        equipamentos = equipamentos.filter(ativo=False)
    elif status == "todos":
        pass
    else:
        status = "ativos"
        equipamentos = equipamentos.filter(ativo=True)

    # Pesquisa por frota, placa ou descrição
    if pesquisa:
        equipamentos = equipamentos.filter(
            Q(frota__icontains=pesquisa)
            | Q(placa__icontains=pesquisa)
            | Q(descricao__icontains=pesquisa)
        )

    equipamentos = equipamentos.order_by("frota")

    # Paginação: 10 equipamentos por página
    paginator = Paginator(equipamentos, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "cadastros/equipamento_list.html",
        {
            "page_obj": page_obj,
            "equipamentos": page_obj,
            "status": status,
            "pesquisa": pesquisa,
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


def equipamento_detail(request, pk):

    equipamento = get_object_or_404(
        Equipamento,
        pk=pk,
    )

    return render(
        request,
        "cadastros/equipamento_detail.html",
        {
            "equipamento": equipamento,
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
