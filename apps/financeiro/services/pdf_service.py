from apps.financeiro.documents.adiantamento_pdf import AdiantamentoPdf


class PdfService:
    @staticmethod
    def gerar(lote):

        documento = AdiantamentoPdf()

        return documento.gerar(lote)
