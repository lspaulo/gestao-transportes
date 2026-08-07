from django.contrib.auth.forms import PasswordChangeForm


class AlterarSenhaForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["old_password"].label = "Senha Atual"
        self.fields["new_password1"].label = "Nova Senha"
        self.fields["new_password2"].label = "Confirmar Nova Senha"

        placeholders = {
            "old_password": "Informe sua senha atual",
            "new_password1": "Informe a nova senha",
            "new_password2": "Confirme a nova senha",
        }

        for nome, campo in self.fields.items():
            campo.widget.attrs["class"] = "form-control"

            campo.widget.attrs["placeholder"] = placeholders[nome]
