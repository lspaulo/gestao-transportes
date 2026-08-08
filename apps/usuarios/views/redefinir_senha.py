from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from apps.usuarios.decorators import perfil_required
from apps.usuarios.forms import RedefinirSenhaForm
from apps.usuarios.models import TipoPerfil
from apps.usuarios.permissions import (
    pode_editar_usuario,
)


@login_required
@perfil_required(
    TipoPerfil.ADMINISTRADOR,
    TipoPerfil.GESTOR,
)
def redefinir_senha(request, pk):

    usuario = get_object_or_404(
        User,
        pk=pk,
    )

    if not pode_editar_usuario(
        request.user,
        usuario,
    ):
        messages.error(
            request,
            "Você não possui permissão para redefinir a senha deste usuário.",
        )

        return redirect("usuarios:usuario_list")

    if not usuario.is_active:
        messages.warning(
            request,
            "Não é possível redefinir a senha de um usuário inativo.",
        )

        return redirect("usuarios:usuario_list")

    if request.method == "POST":
        form = RedefinirSenhaForm(request.POST)

        if form.is_valid():
            usuario.set_password(form.cleaned_data["nova_senha"])

            usuario.save()

            messages.success(
                request,
                "Senha redefinida com sucesso.",
            )

            return redirect(
                "usuarios:usuario_list",
            )

    else:
        form = RedefinirSenhaForm()

    return render(
        request,
        "usuarios/redefinir_senha.html",
        {
            "form": form,
            "usuario": usuario,
        },
    )
