from django import forms

from apps.cadastros.models import ContaBancariaFuncionario


class ContaBancariaFuncionarioForm(forms.ModelForm):
    class Meta:
        model = ContaBancariaFuncionario

        fields = "__all__"

        widgets = {
            "funcionario": forms.Select(attrs={"class": "form-select"}),
            "titular": forms.TextInput(attrs={"class": "form-control"}),
            "banco": forms.Select(attrs={"class": "form-select"}),
            "agencia": forms.TextInput(attrs={"class": "form-control"}),
            "digito_agencia": forms.TextInput(attrs={"class": "form-control"}),
            "numero_conta": forms.TextInput(attrs={"class": "form-control"}),
            "digito_conta": forms.TextInput(attrs={"class": "form-control"}),
            "tipo_conta": forms.Select(attrs={"class": "form-select"}),
            "tipo_chave_pix": forms.Select(attrs={"class": "form-select"}),
            "chave_pix": forms.TextInput(attrs={"class": "form-control"}),
            "padrao": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "observacao": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
        }

    def __init__(self, *args, funcionario=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.funcionario = funcionario

        if funcionario and "funcionario" in self.fields:
            self.fields.pop("funcionario")

        if "titular" in self.fields:
            self.fields.pop("titular")

    def save(self, commit=True):
        conta = super().save(commit=False)

        if self.funcionario:
            conta.funcionario = self.funcionario

        if not conta.titular:
            conta.titular = conta.funcionario.nome

        if commit:
            conta.save()

        return conta
