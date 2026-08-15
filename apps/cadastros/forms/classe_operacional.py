from django import forms

from apps.cadastros.models import ClasseOperacional


class ClasseOperacionalForm(forms.ModelForm):
    class Meta:
        model = ClasseOperacional

        fields = (
            "nome",
            "descricao",
            "possui_placa",
            "ordem",
            "ativo",
        )

        widgets = {
            "descricao": forms.Textarea(
                attrs={
                    "rows": 3,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in self.fields.values():
            if not isinstance(campo.widget, forms.CheckboxInput):
                campo.widget.attrs["class"] = "form-control"

        self.fields["possui_placa"].widget.attrs["class"] = "form-check-input"
        self.fields["ativo"].widget.attrs["class"] = "form-check-input"
