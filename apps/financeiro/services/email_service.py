from django.core.mail import EmailMessage

from .pdf_service import PdfService


def formatar_nome_setor(nome):
    if not nome:
        return "Setor"

    return nome.strip().title()


class EmailService:
    @staticmethod
    def enviar_lotes(lotes):

        if not lotes:
            raise ValueError("Nenhum lote foi informado para envio.")

        primeiro_lote = lotes[0]

        destinatario = primeiro_lote.solicitante.email

        if not destinatario:
            raise ValueError("O usuário solicitante não possui e-mail cadastrado.")

        assunto = (
            f"Solicitações de Adiantamento – "
            f"{len(lotes)} lote(s) – "
            "Gestão de Transportes"
        )

        mensagem = (
            "Prezados,\n\n"
            "Encaminhamos, em anexo, os documentos referentes "
            "às solicitações de adiantamento registradas no "
            "Sistema de Gestão de Transportes.\n\n"
            "Solicitações encaminhadas:\n\n"
        )

        for lote in lotes:
            mensagem += f"• Lote {lote.numero} – {lote.setor_historico}\n"

        mensagem += (
            "\n"
            "Os documentos correspondentes seguem anexados "
            "para prosseguimento do processo.\n\n"
            "Atenciosamente,\n"
            f"Setor de {formatar_nome_setor(primeiro_lote.setor_historico)}"
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
