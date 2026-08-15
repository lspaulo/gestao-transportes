from django import forms

from apps.cadastros.models import Empresa


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa

        fields = (
            "razao_social",
            "nome_fantasia",
            "cnpj",
            "inscricao_estadual",
            "telefone",
            "email",
            "observacao",
            "ativo",
        )

        widgets = {
            "observacao": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in self.fields.values():
            if not isinstance(campo.widget, forms.CheckboxInput):
                campo.widget.attrs["class"] = "form-control"

        self.fields["ativo"].widget.attrs["class"] = "form-check-input"
