from typing import cast

from django import forms

from apps.usuarios.models import (
    PerfilUsuario,
)
from apps.usuarios.permissions import perfis_disponiveis


class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario

        fields = (
            "funcionario",
            "perfil",
        )

    def __init__(self, *args, **kwargs):

        usuario_logado = kwargs.pop("usuario_logado", None)

        super().__init__(*args, **kwargs)

        for campo in self.fields.values():
            if not isinstance(campo.widget, forms.CheckboxInput):
                campo.widget.attrs["class"] = "form-control"

        # Gestor não pode visualizar a opção Administrador
        campo_perfil = cast(
            forms.ChoiceField,
            self.fields["perfil"],
        )

        if usuario_logado:

            campo_perfil.choices = perfis_disponiveis(
                usuario_logado
            )
       