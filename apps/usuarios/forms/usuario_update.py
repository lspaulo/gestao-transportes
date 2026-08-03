from django import forms
from django.contrib.auth.models import User


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User

        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )

        labels = {
            "username": "Usuário",
            "first_name": "Primeiro Nome",
            "last_name": "Sobrenome",
            "email": "E-mail",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "username": "Informe o usuário",
            "first_name": "Informe o primeiro nome",
            "last_name": "Informe o sobrenome",
            "email": "nome@empresa.com",
        }

        for nome, campo in self.fields.items():
            campo.widget.attrs["class"] = "form-control"

            if nome in placeholders:
                campo.widget.attrs["placeholder"] = placeholders[nome]
