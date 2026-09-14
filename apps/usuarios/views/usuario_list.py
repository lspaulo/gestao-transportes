from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

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

    status = request.GET.get("status", "ativos")

    if status == "inativos":
        usuarios = usuarios.filter(is_active=False)

    elif status == "todos":
        pass

    else:
        status = "ativos"
        usuarios = usuarios.filter(is_active=True)

    context = {
        "usuarios": usuarios,
        "status": status,
    }

    return render(
        request,
        "usuarios/usuario_list.html",
        context,
    )


@login_required
@perfil_required(
    TipoPerfil.ADMINISTRADOR,
    TipoPerfil.GESTOR,
)
def usuario_detail(request, pk):

    usuarios = usuarios_visiveis(request.user)

    usuario = get_object_or_404(
        usuarios,
        pk=pk,
    )

    return render(
        request,
        "usuarios/usuario_detail.html",
        {
            "usuario": usuario,
        },
    )
