from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.usuarios.decorators import perfil_required
from apps.usuarios.forms import PerfilUsuarioForm, UserForm  # type: ignore
from apps.usuarios.models import TipoPerfil
from apps.usuarios.permissions import (
    pode_definir_perfil,
)


@login_required
@perfil_required(
    TipoPerfil.ADMINISTRADOR,
    TipoPerfil.GESTOR,
)
def usuario_create(request):

    if request.method == "POST":
        user_form = UserForm(request.POST)
        perfil_form = PerfilUsuarioForm(
            request.POST,
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
            usuario = user_form.save(commit=False)
            usuario.set_password(user_form.cleaned_data["password"])
            usuario.save()

            perfil = perfil_form.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

            messages.success(
                request,
                "Usuário cadastrado com sucesso.",
            )

            return redirect(
                "usuarios:usuario_list",
            )

    else:
        user_form = UserForm()
        perfil_form = PerfilUsuarioForm(
            usuario_logado=request.user,
        )

    return render(
        request,
        "usuarios/usuario_form.html",
        {
            "user_form": user_form,
            "perfil_form": perfil_form,
        },
    )
