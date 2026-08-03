from django import forms
from django.contrib.auth.models import User

from .models import PerfilUsuario


class UserForm(forms.ModelForm):
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = User

        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in self.fields.values():
            campo.widget.attrs["class"] = "form-control"


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
