from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import (
    get_object_or_404,
    redirect,
)


@login_required
def usuario_toggle_status(request, pk):

    usuario = get_object_or_404(
        User,
        pk=pk,
    )

    # Impede que o usuário desative a própria conta
    if usuario == request.user:
        messages.error(
            request,
            "Você não pode inativar sua própria conta.",
        )

        return redirect("usuarios:usuario_list")

    usuario.is_active = not usuario.is_active

    usuario.save()

    if usuario.is_active:
        messages.success(
            request,
            "Usuário ativado com sucesso.",
        )

    else:
        messages.success(
            request,
            "Usuário inativado com sucesso.",
        )

    return redirect("usuarios:usuario_list")
