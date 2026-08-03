from django import forms
from django.contrib.auth.models import User


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
