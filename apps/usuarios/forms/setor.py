from django import forms

from apps.usuarios.models import Setor


class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor

        fields = (
            "nome",
            "responsavel",
            "responsavel_substituto",
            "ativo",
        )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for campo in self.fields.values():
            if not isinstance(
                campo.widget,
                forms.CheckboxInput,
            ):
                campo.widget.attrs["class"] = "form-control"

        self.fields["responsavel"].queryset = self.fields[
            "responsavel"
        ].queryset.order_by("nome")

        self.fields["responsavel_substituto"].queryset = self.fields[
            "responsavel_substituto"
        ].queryset.order_by("nome")
