from dataclasses import dataclass
from decimal import Decimal

from apps.cadastros.models import Empresa
from apps.financeiro.models import Adiantamento


@dataclass(slots=True)
class LoteAdiantamentoDTO:
    empresa: Empresa
    adiantamentos: list[Adiantamento]
    quantidade: int
    total: Decimal
