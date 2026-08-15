from django import forms

from apps.cadastros.models import StatusEquipamento


class StatusEquipamentoForm(forms.ModelForm):
    class Meta:
        model = StatusEquipamento

        fields = (
            "nome",
            "descricao",
            "permite_utilizacao",
            "ordem",
        )

        widgets = {
            "nome": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "descricao": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
            "permite_utilizacao": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "ordem": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),
        }
