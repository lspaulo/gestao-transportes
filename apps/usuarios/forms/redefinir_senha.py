from django import forms
from django.contrib.auth.password_validation import validate_password


class RedefinirSenhaForm(forms.Form):
    nova_senha = forms.CharField(
        label="Nova Senha",
        widget=forms.PasswordInput(),
    )

    confirmar_senha = forms.CharField(
        label="Confirmar Nova Senha",
        widget=forms.PasswordInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "nova_senha": "Informe a nova senha",
            "confirmar_senha": "Confirme a nova senha",
        }

        for nome, campo in self.fields.items():
            campo.widget.attrs["class"] = "form-control"

            campo.widget.attrs["placeholder"] = placeholders[nome]

    def clean_nova_senha(self):

        senha = self.cleaned_data["nova_senha"]

        validate_password(senha)

        return senha

    def clean(self):

        cleaned_data = super().clean()

        senha = cleaned_data.get("nova_senha")

        confirmar = cleaned_data.get("confirmar_senha")

        if senha and confirmar and senha != confirmar:
            raise forms.ValidationError("As senhas informadas não conferem.")

        return cleaned_data
