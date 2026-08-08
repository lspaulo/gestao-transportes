from apps.usuarios.permissions import permissoes_interface


def permissoes(request):

    if not request.user.is_authenticated:
        return {}

    try:
        perfil = request.user.perfil

    except Exception:
        return {}

    contexto = permissoes_interface(request.user)

    contexto.update(
        {
            "perfil_usuario": perfil,
            "is_admin": perfil.is_admin,
            "is_gestor": perfil.is_gestor,
            "is_operador": perfil.is_operador,
        }
    )

    return contexto
