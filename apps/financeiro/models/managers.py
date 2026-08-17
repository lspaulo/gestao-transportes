from django.db import models

from apps.usuarios.models import PerfilUsuario


class AdiantamentoManager(models.Manager):
    def visiveis_para(self, usuario):

        queryset = self.select_related(
            "funcionario",
            "empresa",
            "setor",
            "conta_bancaria",
            "solicitante",
        )

        if usuario.is_superuser:
            return queryset

        perfil = PerfilUsuario.objects.filter(
            usuario=usuario,
        ).first()

        if perfil is None:
            return self.none()

        return queryset.filter(
            setor=perfil.setor,
        )
