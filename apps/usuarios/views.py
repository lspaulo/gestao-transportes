from django.shortcuts import redirect, render

from .forms import PerfilUsuarioForm, UserForm  # type: ignore


def usuario_create(request):

    if request.method == "POST":
        user_form = UserForm(request.POST)
        perfil_form = PerfilUsuarioForm(request.POST)

        if user_form.is_valid() and perfil_form.is_valid():
            usuario = user_form.save(commit=False)
            usuario.set_password(user_form.cleaned_data["password"])
            usuario.save()

            perfil = perfil_form.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

            return redirect("home")

    else:
        user_form = UserForm()
        perfil_form = PerfilUsuarioForm()

    return render(
        request,
        "usuarios/usuario_form.html",
        {
            "user_form": user_form,
            "perfil_form": perfil_form,
        },
    )
