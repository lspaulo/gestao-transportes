from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from apps.cadastros.forms import ClasseOperacionalForm
from apps.cadastros.models import ClasseOperacional  # type: ignore


def classe_operacional_list(request):
    pesquisa = request.GET.get("q", "")
    status = request.GET.get("status", "ativos")

    classes = ClasseOperacional.objects.all()

    if status == "ativos":
        classes = classes.filter(ativo=True)
    elif status == "inativos":
        classes = classes.filter(ativo=False)

    if pesquisa:
        classes = classes.filter(nome__icontains=pesquisa)

    classes = classes.order_by("ordem", "nome")

    paginator = Paginator(classes, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "cadastros/classe_operacional_list.html",
        {
            "page_obj": page_obj,
            "status": status,
        },
    )


def classe_operacional_create(request):

    if request.method == "POST":
        form = ClasseOperacionalForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("cadastros:classe_operacional_list")

    else:
        form = ClasseOperacionalForm()

    return render(
        request,
        "cadastros/classe_operacional_form.html",
        {
            "form": form,
            "titulo": "Nova Classe Operacional",
            "descricao": "Cadastre uma nova classe operacional",
            "icone": "bi-diagram-3",
        },
    )


def classe_operacional_update(request, pk):

    classe = get_object_or_404(
        ClasseOperacional,
        pk=pk,
    )

    if request.method == "POST":
        form = ClasseOperacionalForm(
            request.POST,
            instance=classe,
        )

        if form.is_valid():
            form.save()

            return redirect("cadastros:classe_operacional_list")

    else:
        form = ClasseOperacionalForm(
            instance=classe,
        )

    return render(
        request,
        "cadastros/classe_operacional_form.html",
        {
            "form": form,
            "titulo": "Editar Classe Operacional",
            "descricao": "Edite os dados da classe operacional",
            "icone": "bi-diagram-3",
        },
    )


def classe_operacional_toggle_status(request, pk):

    classe = get_object_or_404(
        ClasseOperacional,
        pk=pk,
    )

    classe.ativo = not classe.ativo

    classe.save()

    return redirect("cadastros:classe_operacional_list")
