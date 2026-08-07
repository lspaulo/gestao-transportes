from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.usuarios.forms import AlterarSenhaForm  # type: ignore


@login_required
def alterar_senha(request):

    if request.method == "POST":
        form = AlterarSenhaForm(
            request.user,
            request.POST,
        )

        if form.is_valid():
            usuario = form.save()

            update_session_auth_hash(
                request,
                usuario,
            )

            messages.success(
                request,
                "Senha alterada com sucesso.",
            )

            return redirect(
                "usuarios:meu_perfil",
            )

    else:
        form = AlterarSenhaForm(request.user)

    return render(
        request,
        "usuarios/alterar_senha.html",
        {
            "form": form,
        },
    )
