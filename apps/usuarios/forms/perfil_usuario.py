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
            "setor",
        )

    def __init__(self, *args, **kwargs):

        self.usuario_logado = kwargs.pop(
            "usuario_logado",
            None,
        )

        super().__init__(*args, **kwargs)

        for campo in self.fields.values():
            if not isinstance(campo.widget, forms.CheckboxInput):
                campo.widget.attrs["class"] = "form-control"

        campo_perfil = cast(
            forms.ChoiceField,
            self.fields["perfil"],
        )

        if self.usuario_logado:
            # Perfis disponíveis conforme o perfil do usuário logado
            campo_perfil.choices = perfis_disponiveis(self.usuario_logado)

            # Se for gestor, limita ao próprio setor
            if self.usuario_logado.perfil.is_gestor:
                self.fields["setor"].queryset = self.fields["setor"].queryset.filter(
                    pk=self.usuario_logado.perfil.setor_id,
                )

                self.fields["setor"].initial = self.usuario_logado.perfil.setor

                self.fields["setor"].disabled = True

    def clean_setor(self):

        setor = self.cleaned_data["setor"]

        usuario_logado = getattr(
            self,
            "usuario_logado",
            None,
        )

        if usuario_logado and usuario_logado.perfil.is_gestor:
            return usuario_logado.perfil.setor

        return setor
