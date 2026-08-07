from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from apps.usuarios.forms import RedefinirSenhaForm


@login_required
def redefinir_senha(request, pk):

    usuario = get_object_or_404(
        User,
        pk=pk,
    )

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
