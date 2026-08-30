import os
from io import BytesIO
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class AdiantamentoPdf:
    def gerar(
        self,
        lote,
    ):
        self._lote_atual = lote

        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            rightMargin=1.2 * cm,
            leftMargin=1.2 * cm,
            topMargin=2.6 * cm,
            bottomMargin=1.5 * cm,
        )

        styles = getSampleStyleSheet()

        elementos = []

        self._tabela(
            elementos,
            lote,
        )

        self._resumo(
            elementos,
            lote,
            styles,
        )

        doc.build(
            elementos,
            onFirstPage=self._cabecalho_e_rodape_canvas,
            onLaterPages=self._cabecalho_e_rodape_canvas,
        )

        buffer.seek(0)

        return buffer

    def _logo(
        self,
        lote,
    ):
        if lote.empresa.logo and os.path.exists(
            lote.empresa.logo.path,
        ):
            imagem = ImageReader(
                lote.empresa.logo.path,
            )

            largura_original, altura_original = imagem.getSize()

            altura_maxima = 1.55 * cm
            largura_maxima = 3.0 * cm

            proporcao = largura_original / altura_original

            altura = altura_maxima
            largura = altura * proporcao

            if largura > largura_maxima:
                largura = largura_maxima
                altura = largura / proporcao

            return Image(
                lote.empresa.logo.path,
                width=largura,
                height=altura,
            )

        return Spacer(
            3.0 * cm,
            1.55 * cm,
        )

    def _cabecalho_canvas(
        self,
        canvas,
        doc,
    ):
        canvas.saveState()

        _, altura = landscape(A4)

        lote = getattr(
            self,
            "_lote_atual",
            None,
        )

        if lote is None:
            canvas.restoreState()
            return

        # ---------------------------------------------------------
        # LOGO
        # ---------------------------------------------------------

        if lote.empresa.logo and os.path.exists(
            lote.empresa.logo.path,
        ):
            imagem = ImageReader(
                lote.empresa.logo.path,
            )

            largura_original, altura_original = imagem.getSize()

            altura_maxima = 1.55 * cm
            largura_maxima = 3.0 * cm

            proporcao = largura_original / altura_original

            altura_logo = altura_maxima
            largura_logo = altura_logo * proporcao

            if largura_logo > largura_maxima:
                largura_logo = largura_maxima
                altura_logo = largura_logo / proporcao

            x_logo = 1.2 * cm
            y_logo = altura - 1.9 * cm

            canvas.drawImage(
                lote.empresa.logo.path,
                x_logo,
                y_logo,
                width=largura_logo,
                height=altura_logo,
                preserveAspectRatio=True,
                mask="auto",
            )

        # ---------------------------------------------------------
        # LINHA VERTICAL
        # ---------------------------------------------------------

        x_linha = 4.4 * cm

        canvas.setStrokeColor(
            colors.HexColor("#D9D9D9"),
        )

        canvas.setLineWidth(0.5)

        canvas.line(
            x_linha,
            altura - 0.7 * cm,
            x_linha,
            altura - 2.15 * cm,
        )

        # ---------------------------------------------------------
        # NOME DA EMPRESA
        # ---------------------------------------------------------

        canvas.setFont(
            "Helvetica-Bold",
            16,
        )

        canvas.setFillColor(
            colors.HexColor("#222222"),
        )

        canvas.drawString(
            x_linha + 0.3 * cm,
            altura - 1.15 * cm,
            lote.empresa.nome_fantasia.upper(),
        )

        # ---------------------------------------------------------
        # RAZÃO SOCIAL
        # ---------------------------------------------------------

        canvas.setFont(
            "Helvetica",
            7.5,
        )

        canvas.setFillColor(
            colors.HexColor("#777777"),
        )

        canvas.drawString(
            x_linha + 0.3 * cm,
            altura - 1.48 * cm,
            lote.empresa.razao_social,
        )

        # ---------------------------------------------------------
        # TÍTULO DO DOCUMENTO
        # ---------------------------------------------------------

        canvas.setFont(
            "Helvetica-Bold",
            10,
        )

        canvas.setFillColor(
            colors.HexColor("#444444"),
        )

        canvas.drawString(
            x_linha + 0.3 * cm,
            altura - 2.05 * cm,
            "SOLICITAÇÃO DE ADIANTAMENTO DE VIAGEM",
        )

        canvas.restoreState()

    def _cabecalho_e_rodape_canvas(
        self,
        canvas,
        doc,
    ):
        self._cabecalho_canvas(
            canvas,
            doc,
        )

        self._rodape_canvas(
            canvas,
            doc,
        )

    def _tabela(
        self,
        elementos,
        lote,
    ):
        dados: list[list[Any]] = [
            [
                "Motorista",
                "CPF",
                "Banco",
                "Agência",
                "Conta",
                "Tipo",
                "PIX",
                "Valor",
            ]
        ]

        adiantamentos = sorted(
            lote.adiantamentos.all(),
            key=lambda adiantamento: (
                adiantamento.historico_nome_motorista or ""
            ).upper(),
        )

        for adiantamento in adiantamentos:
            valor = (
                f"{adiantamento.valor:,.2f}".replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

            agencia = adiantamento.historico_agencia or ""

            if adiantamento.historico_digito_agencia:
                agencia += f"-{adiantamento.historico_digito_agencia}"

            numero_conta = adiantamento.historico_numero_conta or ""

            if adiantamento.historico_digito_conta:
                numero_conta += f"-{adiantamento.historico_digito_conta}"

            pix = (
                f"<b>{adiantamento.historico_tipo_chave_pix}</b>"
                f"<br/>{adiantamento.historico_chave_pix}"
            )

            dados.append(
                [
                    Paragraph(
                        adiantamento.historico_nome_motorista or "",
                        self._estilo_tabela(),
                    ),
                    Paragraph(
                        adiantamento.historico_cpf_motorista or "",
                        self._estilo_tabela(),
                    ),
                    Paragraph(
                        adiantamento.historico_banco or "",
                        self._estilo_tabela(),
                    ),
                    Paragraph(
                        agencia,
                        self._estilo_tabela(),
                    ),
                    Paragraph(
                        numero_conta,
                        self._estilo_tabela(),
                    ),
                    Paragraph(
                        adiantamento.historico_tipo_conta or "",
                        self._estilo_tabela(),
                    ),
                    Paragraph(
                        pix,
                        self._estilo_tabela(),
                    ),
                    Paragraph(
                        f"R$ {valor}",
                        self._estilo_tabela_direita(),
                    ),
                ]
            )

        tabela = Table(
            dados,
            colWidths=[
                6.0 * cm,  # Motorista
                3 * cm,  # CPF
                3 * cm,  # Banco
                2.0 * cm,  # Agência
                2.5 * cm,  # Conta
                2.5 * cm,  # Tipo
                4 * cm,  # PIX
                3.0 * cm,  # Valor
            ],
            repeatRows=1,
        )

        tabela.hAlign = "LEFT"

        tabela.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#2F7D44"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.HexColor("#CCCCCC"),
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, 0),
                        7,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, 0),
                        7,
                    ),
                    (
                        "ALIGN",
                        (7, 1),
                        (7, -1),
                        "RIGHT",
                    ),
                ]
            )
        )

        elementos.append(tabela)

        elementos.append(
            Spacer(
                1,
                0.5 * cm,
            )
        )

    def _resumo(
        self,
        elementos,
        lote,
        styles,
    ):
        estilo_quantidade = ParagraphStyle(
            "ResumoQuantidade",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=10,
            alignment=1,
        )

        estilo_total = ParagraphStyle(
            "ResumoTotal",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=12,
            alignment=1,
        )

        quantidade = Paragraph(
            f"<b>Quantidade de Motoristas:</b> {lote.quantidade}",
            estilo_quantidade,
        )

        total = Paragraph(
            f"<b>Total: R$ {lote.total_formatado}</b>",
            estilo_total,
        )

        resumo = Table(
            [
                [
                    quantidade,
                    total,
                ]
            ],
            colWidths=[
                8.75 * cm,
                8.75 * cm,
            ],
        )

        resumo.hAlign = "CENTER"

        resumo.setStyle(
            TableStyle(
                [
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.HexColor("#CCCCCC"),
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "ALIGN",
                        (0, 0),
                        (-1, -1),
                        "CENTER",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                ]
            )
        )

        elementos.append(resumo)

        elementos.append(
            Spacer(
                1,
                0.35 * cm,
            )
        )

    def _rodape_canvas(
        self,
        canvas,
        doc,
    ):
        canvas.saveState()

        largura, altura = landscape(A4)

        lote = getattr(
            self,
            "_lote_atual",
            None,
        )

        if lote is not None:
            emitido_por = lote.solicitante.get_full_name() or lote.solicitante.username

            responsavel = (
                str(lote.setor.responsavel)
                if lote.setor and lote.setor.responsavel
                else "Não informado"
            )

            setor = str(lote.setor) if lote.setor else "Não informado"

            data_emissao = lote.data_emissao.strftime("%d/%m/%Y às %H:%M")

            # -------------------------------------------------
            # LINHA VERDE DO RODAPÉ
            # -------------------------------------------------

            canvas.setStrokeColor(colors.HexColor("#2F7D44"))

            canvas.setLineWidth(0.7)

            canvas.line(
                1.2 * cm,
                1.35 * cm,
                largura - 1.2 * cm,
                1.35 * cm,
            )

            # -------------------------------------------------
            # ESTILO DO TEXTO
            # -------------------------------------------------

            canvas.setFont(
                "Helvetica",
                7.5,
            )

            canvas.setFillColor(colors.HexColor("#555555"))

            # -------------------------------------------------
            # LADO ESQUERDO
            # -------------------------------------------------

            x_esquerda = 1.2 * cm

            canvas.drawString(
                x_esquerda,
                0.95 * cm,
                f"Emitido por: {emitido_por}",
            )

            canvas.drawString(
                x_esquerda,
                0.62 * cm,
                f"Lote: {lote.numero}",
            )

            canvas.drawString(
                x_esquerda,
                0.29 * cm,
                f"Data: {data_emissao}",
            )

            # -------------------------------------------------
            # LADO DIREITO
            # -------------------------------------------------

            x_direita = largura - 1.2 * cm

            canvas.drawRightString(
                x_direita,
                0.95 * cm,
                f"Responsável: {responsavel}",
            )

            canvas.drawRightString(
                x_direita,
                0.62 * cm,
                f"Setor: {setor}",
            )

            canvas.drawRightString(
                x_direita,
                0.29 * cm,
                "Sistema Gestão de Transportes",
            )

        canvas.restoreState()

    def _estilo_tabela(self):
        return ParagraphStyle(
            "Tabela",
            fontName="Helvetica",
            fontSize=8,
            leading=9,
        )

    def _estilo_tabela_direita(self):
        return ParagraphStyle(
            "TabelaDireita",
            fontName="Helvetica",
            fontSize=8,
            leading=9,
            alignment=2,
        )
