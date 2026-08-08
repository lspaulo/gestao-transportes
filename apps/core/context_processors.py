def permissoes(request):

    if not request.user.is_authenticated:
        return {}

    try:
        perfil = request.user.perfil

    except Exception:
        return {}

    return {
        "is_admin": perfil.is_admin,
        "is_gestor": perfil.is_gestor,
        "is_operador": perfil.is_operador,
        "perfil_usuario": perfil,
        "tipo_perfil": perfil.perfil,
    }
