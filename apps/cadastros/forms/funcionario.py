from django import forms

from apps.cadastros.models import Funcionario
from apps.core.validators.cpf import normalizar_cpf, validar_cpf


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = "__all__"

        widgets = {
            # Dados pessoais
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            # Dados profissionais
            "data_admissao": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "matricula": forms.TextInput(attrs={"class": "form-control"}),
            "codigo_fornecedor": forms.TextInput(attrs={"class": "form-control"}),
            "empresa": forms.Select(attrs={"class": "form-select"}),
            "funcao": forms.Select(attrs={"class": "form-select"}),
            # Habilitação
            "numero_cnh": forms.TextInput(attrs={"class": "form-control"}),
            "validade_cnh": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            # Endereço
            "cep": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "00000-000",
                    "maxlength": "9",
                }
            ),
            "logradouro": forms.TextInput(attrs={"class": "form-control"}),
            "numero_endereco": forms.TextInput(attrs={"class": "form-control"}),
            "complemento": forms.TextInput(attrs={"class": "form-control"}),
            "bairro": forms.TextInput(attrs={"class": "form-control"}),
            "cidade": forms.TextInput(attrs={"class": "form-control"}),
            "uf": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": "2",
                    "placeholder": "Ex.: AL",
                }
            ),
            # Informações complementares
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
            # Situação cadastral
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_cpf(self):
        cpf = normalizar_cpf(self.cleaned_data.get("cpf"))

        if not validar_cpf(cpf):
            raise forms.ValidationError("Informe um CPF válido, com 11 dígitos.")

        return cpf

    def clean_uf(self):
        uf = self.cleaned_data.get("uf", "")
        return uf.strip().upper()
