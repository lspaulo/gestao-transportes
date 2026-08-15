from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import StatusEquipamentoForm
from ..models import StatusEquipamento


@login_required
def status_operacional_list(request):

    status_operacionais = StatusEquipamento.objects.all()

    return render(
        request,
        "cadastros/status_operacional_list.html",
        {
            "status_operacionais": status_operacionais,
        },
    )


@login_required
def status_operacional_create(request):

    if request.method == "POST":
        form = StatusEquipamentoForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Status operacional cadastrado com sucesso.",
            )

            return redirect("cadastros:status_operacional_list")

    else:
        form = StatusEquipamentoForm()

    return render(
        request,
        "cadastros/status_operacional_form.html",
        {
            "form": form,
            "titulo": "Novo Status Operacional",
            "descricao": "Cadastre um novo status operacional",
            "icone": "bi-activity",
        },
    )


@login_required
def status_operacional_update(request, pk):

    status = get_object_or_404(
        StatusEquipamento,
        pk=pk,
    )

    if request.method == "POST":
        form = StatusEquipamentoForm(
            request.POST,
            instance=status,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Status operacional atualizado com sucesso.",
            )

            return redirect("cadastros:status_operacional_list")

    else:
        form = StatusEquipamentoForm(
            instance=status,
        )

    return render(
        request,
        "cadastros/status_operacional_form.html",
        {
            "form": form,
            "titulo": "Editar Status Operacional",
            "descricao": "Edite os dados do status operacional",
            "icone": "bi-activity",
        },
    )


@login_required
def status_operacional_toggle_status(request, pk):

    status_operacional = get_object_or_404(
        StatusEquipamento,
        pk=pk,
    )

    status_operacional.ativo = not status_operacional.ativo

    status_operacional.save()

    return redirect("cadastros:status_operacional_list")
