from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from apps.usuarios.decorators import perfil_required
from apps.usuarios.forms import (
    PerfilUsuarioForm,
    UserUpdateForm,  # type: ignore
)
from apps.usuarios.models import PerfilUsuario, TipoPerfil
from apps.usuarios.permissions import (
    pode_definir_perfil,
    pode_editar_usuario,
)


@login_required
@perfil_required(
    TipoPerfil.ADMINISTRADOR,
    TipoPerfil.GESTOR,
)
def usuario_update(request, pk):

    usuario = get_object_or_404(
        User,
        pk=pk,
    )

    # Verifica permissão antes de qualquer processamento
    if not pode_editar_usuario(
        request.user,
        usuario,
    ):
        messages.error(
            request,
            "Você não possui permissão para editar este usuário.",
        )

        return redirect("usuarios:usuario_list")

    perfil, _ = PerfilUsuario.objects.get_or_create(
        usuario=usuario,
    )

    if not usuario.is_active:
        messages.warning(
            request,
            "Não é possível editar um usuário inativo.",
        )

        return redirect("usuarios:usuario_list")

    if request.method == "POST":
        user_form = UserUpdateForm(
            request.POST,
            instance=usuario,
        )

        perfil_form = PerfilUsuarioForm(
            request.POST,
            instance=perfil,
            usuario_logado=request.user,
        )

        if user_form.is_valid() and perfil_form.is_valid():
            novo_perfil = perfil_form.cleaned_data["perfil"]

            if not pode_definir_perfil(
                request.user,
                novo_perfil,
            ):
                messages.error(
                    request,
                    "Você não pode atribuir este perfil.",
                )

                return redirect("usuarios:usuario_list")

            user_form.save()
            perfil_form.save()

            messages.success(
                request,
                "Usuário atualizado com sucesso.",
            )

            return redirect("usuarios:usuario_list")

    else:
        user_form = UserUpdateForm(instance=usuario)
        perfil_form = PerfilUsuarioForm(
            instance=perfil,
            usuario_logado=request.user,
        )

    return render(
        request,
        "usuarios/usuario_form.html",
        {
            "user_form": user_form,
            "perfil_form": perfil_form,
            "titulo": "Editar Usuário",
            "descricao": "Atualize os dados do usuário.",
            "icone": "bi-person-badge",
        },
    )
