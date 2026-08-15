from django import forms

from apps.cadastros.models import Equipamento, StatusEquipamento


class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento

        fields = (
            "frota",
            "empresa",
            "classe_operacional",
            "status_operacional",
            "placa",
            "descricao",
            "marca",
            "modelo",
            "ano_fabricacao",
            "ano_modelo",
            "renavam",
            "chassi",
            "cor",
            "observacao",
            "ativo",
        )

        widgets = {
            "observacao": forms.Textarea(
                attrs={
                    "rows": 3,
                }
            ),
            "status_operacional": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["status_operacional"].queryset = StatusEquipamento.objects.filter(  # type:ignore
            ativo=True
        )

        for campo in self.fields.values():
            if isinstance(campo.widget, forms.CheckboxInput):
                campo.widget.attrs["class"] = "form-check-input"

            elif isinstance(campo.widget, forms.Select):
                campo.widget.attrs["class"] = "form-select"

            else:
                campo.widget.attrs["class"] = "form-control"
