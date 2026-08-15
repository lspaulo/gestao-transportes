from django import forms

from apps.cadastros.models import Funcionario


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = "__all__"

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "numero_cnh": forms.TextInput(attrs={"class": "form-control"}),
            "validade_cnh": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "funcao": forms.Select(attrs={"class": "form-select"}),
            "empresa": forms.Select(attrs={"class": "form-select"}),
            "cursos": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
            "observacao": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
