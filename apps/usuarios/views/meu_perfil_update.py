from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.usuarios.forms.meu_perfil import MeuPerfilForm


@login_required
def meu_perfil_update(request):

    if request.method == "POST":
        form = MeuPerfilForm(
            request.POST,
            instance=request.user,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Perfil atualizado com sucesso.",
            )

            return redirect("usuarios:meu_perfil")

    else:
        form = MeuPerfilForm(
            instance=request.user,
        )

    return render(
        request,
        "usuarios/meu_perfil_form.html",
        {
            "form": form,
            "titulo": "Editar Perfil",
            "descricao": "Atualize suas informações pessoais.",
            "icone": "bi-person-circle",
        },
    )
