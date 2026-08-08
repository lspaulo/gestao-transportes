from django.contrib.auth.models import User

from apps.usuarios.models import TipoPerfil


def pode_editar_usuario(usuario_logado, usuario_editado):

    perfil_logado = usuario_logado.perfil
    perfil_editado = usuario_editado.perfil

    # Administrador pode editar qualquer usuário
    if perfil_logado.is_admin:
        return True

    # Gestor pode editar apenas Operadores
    if perfil_logado.is_gestor:
        return perfil_editado.is_operador

    # Operadores não editam usuários
    return False


def pode_definir_perfil(usuario_logado, novo_perfil):

    perfil_logado = usuario_logado.perfil

    if perfil_logado.is_admin:
        return True

    if perfil_logado.is_gestor:
        return novo_perfil == TipoPerfil.OPERADOR

    return False


def perfis_disponiveis(usuario):

    if usuario.perfil.is_admin:
        return TipoPerfil.choices

    if usuario.perfil.is_gestor:
        return [
            (
                TipoPerfil.OPERADOR,
                "Operador",
            )
        ]

    return [
        (
            TipoPerfil.OPERADOR,
            "Operador",
        )
    ]


def usuarios_visiveis(usuario_logado):

    queryset = User.objects.select_related("perfil")

    if usuario_logado.perfil.is_admin:
        return queryset

    if usuario_logado.perfil.is_gestor:
        return queryset.filter(
            perfil__perfil=TipoPerfil.OPERADOR,
        )

    return queryset.filter(
        pk=usuario_logado.pk,
    )


# ==========================
# Permissões por funcionalidade
# ==========================


def pode_gerenciar_usuarios(usuario):

    return usuario.perfil.is_admin or usuario.perfil.is_gestor


def pode_cadastrar_funcionarios(usuario):

    return True


def pode_cadastrar_empresas(usuario):

    return True


def pode_cadastrar_equipamentos(usuario):

    return True


def pode_cadastrar_classes_operacionais(usuario):

    return True


def pode_ver_relatorios(usuario):

    return usuario.perfil.is_admin or usuario.perfil.is_gestor
