from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse

from apps.usuarios.decorators import perfil_required
from apps.usuarios.forms import (
    SetorForm,
)
from apps.usuarios.models import (
    PerfilUsuario,
    Setor,
    TipoPerfil,
)


@login_required
@perfil_required(
    TipoPerfil.ADMINISTRADOR,
)
def setor_list(request):

    setores = Setor.objects.all()

    return render(
        request,
        "usuarios/setor_list.html",
        {
            "setores": setores,
            "titulo": "Setores",
            "descricao": "Cadastro de setores da empresa.",
            "icone": "bi-diagram-3",
        },
    )


@login_required
@perfil_required(
    TipoPerfil.ADMINISTRADOR,
)
def setor_create(request):

    if request.method == "POST":
        form = SetorForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Setor cadastrado com sucesso.",
            )

            return redirect(
                "usuarios:setor_list",
            )

    else:
        form = SetorForm()

    return render(
        request,
        "usuarios/setor_form.html",
        {
            "form": form,
            "titulo": "Novo Setor",
            "descricao": "Cadastre um novo setor.",
            "icone": "bi-diagram-3",
        },
    )


@login_required
@perfil_required(
    TipoPerfil.ADMINISTRADOR,
)
def setor_update(
    request,
    pk,
):

    setor = get_object_or_404(
        Setor,
        pk=pk,
    )

    if request.method == "POST":
        form = SetorForm(
            request.POST,
            instance=setor,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Setor atualizado com sucesso.",
            )

            return redirect(
                "usuarios:setor_list",
            )

    else:
        form = SetorForm(
            instance=setor,
        )

    return render(
        request,
        "usuarios/setor_form.html",
        {
            "form": form,
            "titulo": "Editar Setor",
            "descricao": "Atualize os dados do setor.",
            "icone": "bi-diagram-3",
        },
    )


@login_required
@perfil_required(
    TipoPerfil.ADMINISTRADOR,
)
def setor_delete(
    request,
    pk,
):

    setor = get_object_or_404(
        Setor,
        pk=pk,
    )

    # Validação
    if PerfilUsuario.objects.filter(
        setor=setor,
    ).exists():
        messages.error(
            request,
            "Não é possível excluir um setor que possui usuários vinculados.",
        )

        return redirect(
            "usuarios:setor_list",
        )

    if request.method == "POST":
        setor.delete()

        messages.success(
            request,
            "Setor excluído com sucesso.",
        )

        return redirect(
            "usuarios:setor_list",
        )

    return render(
        request,
        "components/confirm_delete.html",
        {
            "objeto": setor,
            "titulo": "Excluir Setor",
            "url_cancelar": reverse(
                "usuarios:setor_list",
            ),
        },
    )
