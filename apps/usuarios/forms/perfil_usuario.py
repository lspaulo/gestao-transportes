from django import forms

from apps.usuarios.models import PerfilUsuario


class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario

        fields = (
            "funcionario",
            "perfil",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in self.fields.values():
            if not isinstance(campo.widget, forms.CheckboxInput):
                campo.widget.attrs["class"] = "form-control"
