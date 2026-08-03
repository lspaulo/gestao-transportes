from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from apps.usuarios.forms import (
    PerfilUsuarioForm,
    UserUpdateForm,  # type: ignore
)
from apps.usuarios.models import PerfilUsuario


def usuario_update(request, pk):

    usuario = get_object_or_404(User, pk=pk)

    perfil, _ = PerfilUsuario.objects.get_or_create(usuario=usuario)

    if request.method == "POST":
        user_form = UserUpdateForm(
            request.POST,
            instance=usuario,
        )

        perfil_form = PerfilUsuarioForm(
            request.POST,
            instance=perfil,
        )

        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()

            messages.success(
                request,
                "Usuário atualizado com sucesso.",
            )

            return redirect("usuarios:usuario_list")

    else:
        user_form = UserUpdateForm(instance=usuario)
        perfil_form = PerfilUsuarioForm(instance=perfil)

    return render(
        request,
        "usuarios/usuario_form.html",
        {
            "user_form": user_form,
            "perfil_form": perfil_form,
            "titulo": "Editar Usuário",
        },
    )
