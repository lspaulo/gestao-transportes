from django import forms

from apps.cadastros.models import Funcao


class FuncaoForm(forms.ModelForm):
    class Meta:
        model = Funcao

        fields = (
            "nome",
            "descricao",
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
        }
