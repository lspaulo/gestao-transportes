from django.core.mail import EmailMessage

from .pdf_service import PdfService


class EmailService:
    @staticmethod
    def enviar_lotes(lotes):
        if not lotes:
            raise ValueError("Nenhum lote foi informado para envio.")

        primeiro_lote = lotes[0]

        destinatario = primeiro_lote.solicitante.email

        if not destinatario:
            raise ValueError("O usuário solicitante não possui e-mail cadastrado.")

        assunto = f"Solicitação de Adiantamento – {len(lotes)} lote(s)"

        mensagem = (
            "Prezado(a),\n\n"
            "Foram gerados lote(s) de solicitações de "
            "adiantamento no Sistema de Gestão de Transportes.\n\n"
        )

        for lote in lotes:
            mensagem += f"Lote: {lote.numero}\nSetor: {lote.setor_historico}\n\n"

        mensagem += (
            "Os documentos em PDF seguem anexados para conferência.\n\n"
            "Favor verificar os dados, valores e demais informações "
            "antes de encaminhar aos setores responsáveis.\n\n"
            "Atenciosamente,\n"
            "Sistema de Gestão de Transportes"
        )

        email = EmailMessage(
            subject=assunto,
            body=mensagem,
            to=[destinatario],
        )

        for lote in lotes:
            pdf_buffer = PdfService.gerar(lote)
            pdf_buffer.seek(0)

            email.attach(
                f"{lote.numero}.pdf",
                pdf_buffer.getvalue(),
                "application/pdf",
            )

        email.send(fail_silently=False)
