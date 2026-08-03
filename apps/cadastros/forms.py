from django import forms

from .models import (
    ClasseOperacional,  # type: ignore
    Empresa,  # type: ignore
    Equipamento,
    Funcionario,
)


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


class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento

        fields = (
            "frota",
            "empresa",
            "classe_operacional",
            "status",
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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in self.fields.values():
            if not isinstance(campo.widget, forms.CheckboxInput):
                campo.widget.attrs["class"] = "form-control"

        self.fields["ativo"].widget.attrs["class"] = "form-check-input"


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
