from apps.usuarios.permissions import (
    pode_cadastrar_classes_operacionais,
    pode_cadastrar_empresas,
    pode_cadastrar_equipamentos,
    pode_cadastrar_funcionarios,
    pode_gerenciar_usuarios,
    pode_ver_relatorios,
)


def permissoes(request):

    if not request.user.is_authenticated:
        return {}

    try:
        perfil = request.user.perfil

    except Exception:
        return {}

    return {
        "perfil_usuario": perfil,
        "is_admin": perfil.is_admin,
        "is_gestor": perfil.is_gestor,
        "is_operador": perfil.is_operador,
        "pode_gerenciar_usuarios": pode_gerenciar_usuarios(request.user),
        "pode_cadastrar_funcionarios": pode_cadastrar_funcionarios(request.user),
        "pode_cadastrar_empresas": pode_cadastrar_empresas(request.user),
        "pode_cadastrar_equipamentos": pode_cadastrar_equipamentos(request.user),
        "pode_cadastrar_classes_operacionais": pode_cadastrar_classes_operacionais(
            request.user
        ),
        "pode_ver_relatorios": pode_ver_relatorios(request.user),
    }
