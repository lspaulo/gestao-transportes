from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.usuarios.decorators import perfil_required
from apps.usuarios.models import TipoPerfil
from apps.usuarios.permissions import usuarios_visiveis


@login_required
@perfil_required(
    TipoPerfil.ADMINISTRADOR,
    TipoPerfil.GESTOR,
)
def usuario_list(request):

    usuarios = usuarios_visiveis(request.user)

    context = {
        "usuarios": usuarios,
    }

    return render(
        request,
        "usuarios/usuario_list.html",
        context,
    )
