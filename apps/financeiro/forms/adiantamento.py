from django import forms
from django.core.exceptions import ValidationError

from apps.cadastros.models import (
    ContaBancariaFuncionario,
)
from apps.financeiro.models import Adiantamento
from apps.usuarios.models import PerfilUsuario


class AdiantamentoForm(forms.ModelForm):
    empresa = forms.CharField(
        label="Empresa",
        required=False,
        disabled=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "id_empresa",
            }
        ),
    )

    class Meta:
        model = Adiantamento

        fields = (
            "funcionario",
            "conta_bancaria",
            "valor",
            "finalidade",
            "observacao",
        )

        widgets = {
            "funcionario": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "id_funcionario",
                    "data-url": "/financeiro/api/funcionarios/",
                }
            ),
            "conta_bancaria": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "id_conta_bancaria",
                }
            ),
            "valor": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                }
            ),
            "finalidade": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "observacao": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
        }

    def __init__(self, *args, usuario=None, **kwargs):

        super().__init__(*args, **kwargs)

        self.usuario = usuario

        self.fields["conta_bancaria"].queryset = ContaBancariaFuncionario.objects.none()  # type: ignore

        # Edição
        if self.instance.pk:
            contas = ContaBancariaFuncionario.objects.filter(
                funcionario=self.instance.funcionario,
            )

            self.fields["conta_bancaria"].queryset = contas  # type: ignore

        # Cadastro após POST
        elif self.data.get("funcionario"):
            try:
                funcionario_id = int(self.data.get("funcionario"))  # type:ignore

                contas = ContaBancariaFuncionario.objects.filter(
                    funcionario_id=funcionario_id,
                )

                self.fields["conta_bancaria"].queryset = contas  # type: ignore

            except (ValueError, TypeError):
                pass

    def save(self, commit=True):

        adiantamento = super().save(commit=False)
        if not adiantamento.conta_bancaria_id:
            conta_padrao = ContaBancariaFuncionario.objects.filter(
                funcionario=adiantamento.funcionario,
                padrao=True,
            ).first()

            if conta_padrao:
                adiantamento.conta_bancaria = conta_padrao

        if self.usuario:
            adiantamento.solicitante = self.usuario

            perfil = PerfilUsuario.objects.get(
                usuario=self.usuario,
            )

            adiantamento.setor = perfil.setor

        if commit:
            adiantamento.save()

        return adiantamento

    def clean(self):

        cleaned_data = super().clean()

        funcionario = cleaned_data.get("funcionario")
        conta = cleaned_data.get("conta_bancaria")

        if funcionario:
            contas = ContaBancariaFuncionario.objects.filter(
                funcionario=funcionario,
            )

            if not contas.exists():
                raise ValidationError(
                    f"O motorista {funcionario.nome} não possui "
                    "conta bancária cadastrada."
                )

            if conta and conta.funcionario != funcionario:
                raise ValidationError(
                    "A conta bancária selecionada não pertence ao motorista informado."
                )

        return cleaned_data
