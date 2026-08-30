from collections import defaultdict

from django.db import transaction

from apps.financeiro.dto import LoteAdiantamentoDTO
from apps.financeiro.models import (
    Adiantamento,
    LoteAdiantamento,
    StatusAdiantamento,
)


class AdiantamentoService:
    """
    Centraliza as regras de negócio dos
    processos de Adiantamento.
    """

    @staticmethod
    def montar_lotes(
        usuario,
        ids,
    ):

        adiantamentos = Adiantamento.objects.visiveis_para(usuario).filter(  # type: ignore
            id__in=ids,
            lote__isnull=True,
        )

        agrupados = defaultdict(list)

        for adiantamento in adiantamentos:
            agrupados[adiantamento.empresa].append(
                adiantamento,
            )

        lotes = []

        for empresa, itens in agrupados.items():
            lotes.append(
                LoteAdiantamentoDTO(
                    empresa=empresa,
                    adiantamentos=itens,
                    quantidade=len(itens),
                    total=sum(item.valor for item in itens),  # type: ignore
                )
            )

        return lotes

    @staticmethod
    @transaction.atomic
    def emitir_lotes(usuario, ids):

        lotes_dto = AdiantamentoService.montar_lotes(
            usuario,
            ids,
        )

        lotes_criados = []

        for lote_dto in lotes_dto:
            lote = LoteAdiantamento.objects.create(
                empresa=lote_dto.empresa,
                solicitante=usuario,
                setor=usuario.perfil.setor,
            )

            for adiantamento in lote_dto.adiantamentos:
                adiantamento.lote = lote
                adiantamento.status = StatusAdiantamento.SOLICITADO

                adiantamento.save(
                    update_fields=[
                        "lote",
                        "status",
                    ],
                )

            lotes_criados.append(lote)

        return lotes_criados
