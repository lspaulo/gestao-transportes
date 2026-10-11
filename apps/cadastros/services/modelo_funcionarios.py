from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import (
    Alignment,
    Border,
    Font,
    PatternFill,
    Side,
)
from openpyxl.worksheet.datavalidation import (
    DataValidation,
)

from apps.cadastros.models import Empresa, Funcao
from apps.cadastros.models.bancos import Banco
from apps.cadastros.models.conta_bancaria_funcionario import (
    ContaBancariaFuncionario,
)


def criar_modelo_funcionarios():
    workbook = Workbook()

    primeira_planilha = workbook.worksheets[0]

    workbook.remove(primeira_planilha)

    ws_funcionarios = workbook.create_sheet(title="Funcionarios")

    ws_contas = workbook.create_sheet(title="ContasBancarias")

    ws_listas = workbook.create_sheet(title="Listas")

    # ==========================================================
    # ESTILO
    # ==========================================================

    preenchimento_cabecalho = PatternFill(
        fill_type="solid",
        fgColor="198754",
    )

    fonte_cabecalho = Font(
        bold=True,
        color="FFFFFF",
    )

    borda = Border(
        bottom=Side(
            style="thin",
            color="D9D9D9",
        )
    )

    alinhamento = Alignment(
        vertical="center",
    )

    # ==========================================================
    # ABA FUNCIONÁRIOS
    # ==========================================================

    colunas_funcionarios = [
        "Nome",
        "CPF",
        "E-mail",
        "Telefone",
        "Número CNH",
        "Validade CNH",
        "Função",
        "Empresa",
        "Cursos",
        "Observações",
    ]

    for coluna, titulo in enumerate(
        colunas_funcionarios,
        start=1,
    ):
        cell = ws_funcionarios.cell(
            row=1,
            column=coluna,
            value=titulo,
        )

        cell.fill = preenchimento_cabecalho
        cell.font = fonte_cabecalho
        cell.alignment = alinhamento
        cell.border = borda

    # ==========================================================
    # ABA CONTAS BANCÁRIAS
    # ==========================================================

    colunas_contas = [
        "CPF Funcionário",
        "Banco",
        "Agência",
        "Dígito Agência",
        "Número Conta",
        "Dígito Conta",
        "Tipo Conta",
        "Tipo Chave PIX",
        "Chave PIX",
        "Conta Padrão",
        "Observação",
    ]

    for coluna, titulo in enumerate(
        colunas_contas,
        start=1,
    ):
        cell = ws_contas.cell(
            row=1,
            column=coluna,
            value=titulo,
        )

        cell.fill = preenchimento_cabecalho
        cell.font = fonte_cabecalho
        cell.alignment = alinhamento
        cell.border = borda

    # ==========================================================
    # LISTAS AUXILIARES
    # ==========================================================

    ws_listas["A1"] = "Empresas"
    ws_listas["B1"] = "Funções"
    ws_listas["C1"] = "Bancos"
    ws_listas["D1"] = "Tipos de Conta"
    ws_listas["E1"] = "Tipos de Chave PIX"
    ws_listas["F1"] = "Sim/Não"

    for cell in ws_listas[1]:
        cell.font = Font(bold=True)

    empresas = list(Empresa.objects.all().order_by("razao_social"))

    for linha, empresa in enumerate(
        empresas,
        start=2,
    ):
        nome = empresa.nome_fantasia or empresa.razao_social

        ws_listas.cell(
            row=linha,
            column=1,
            value=nome,
        )

    funcoes = list(Funcao.objects.all().order_by("nome"))

    for linha, funcao in enumerate(
        funcoes,
        start=2,
    ):
        ws_listas.cell(
            row=linha,
            column=2,
            value=funcao.nome,
        )

    for linha, (codigo, descricao) in enumerate(
        Banco.choices,
        start=2,
    ):
        ws_listas.cell(
            row=linha,
            column=3,
            value=f"{codigo} - {descricao}",
        )

    for linha, (_, descricao) in enumerate(
        ContaBancariaFuncionario.TipoConta.choices,
        start=2,
    ):
        ws_listas.cell(
            row=linha,
            column=4,
            value=descricao,
        )

    for linha, (_, descricao) in enumerate(
        ContaBancariaFuncionario.TipoChavePix.choices,
        start=2,
    ):
        ws_listas.cell(
            row=linha,
            column=5,
            value=descricao,
        )

    ws_listas["F2"] = "SIM"
    ws_listas["F3"] = "NÃO"

    # ==========================================================
    # LISTAS SUSPENSAS
    # ==========================================================

    if empresas:
        ultima_empresa = len(empresas) + 1

        dv_empresa = DataValidation(
            type="list",
            formula1=(f"=Listas!$A$2:$A${ultima_empresa}"),
            allow_blank=False,
        )

        ws_funcionarios.add_data_validation(dv_empresa)

        dv_empresa.add("H2:H1001")

    if funcoes:
        ultima_funcao = len(funcoes) + 1

        dv_funcao = DataValidation(
            type="list",
            formula1=(f"=Listas!$B$2:$B${ultima_funcao}"),
            allow_blank=True,
        )

        ws_funcionarios.add_data_validation(dv_funcao)

        dv_funcao.add("G2:G1001")

    total_bancos = len(Banco.choices) + 1

    dv_banco = DataValidation(
        type="list",
        formula1=(f"=Listas!$C$2:$C${total_bancos}"),
        allow_blank=False,
    )

    ws_contas.add_data_validation(dv_banco)

    dv_banco.add("B2:B1001")

    total_tipos_conta = len(ContaBancariaFuncionario.TipoConta.choices) + 1

    dv_tipo_conta = DataValidation(
        type="list",
        formula1=(f"=Listas!$D$2:$D${total_tipos_conta}"),
        allow_blank=False,
    )

    ws_contas.add_data_validation(dv_tipo_conta)

    dv_tipo_conta.add("G2:G1001")

    total_tipos_pix = len(ContaBancariaFuncionario.TipoChavePix.choices) + 1

    dv_tipo_pix = DataValidation(
        type="list",
        formula1=(f"=Listas!$E$2:$E${total_tipos_pix}"),
        allow_blank=False,
    )

    ws_contas.add_data_validation(dv_tipo_pix)

    dv_tipo_pix.add("H2:H1001")

    dv_sim_nao = DataValidation(
        type="list",
        formula1="=Listas!$F$2:$F$3",
        allow_blank=True,
    )

    ws_contas.add_data_validation(dv_sim_nao)

    dv_sim_nao.add("J2:J1001")

    # ==========================================================
    # FORMATAÇÃO
    # ==========================================================

    larguras_funcionarios = {
        "A": 30,
        "B": 18,
        "C": 30,
        "D": 18,
        "E": 18,
        "F": 18,
        "G": 25,
        "H": 30,
        "I": 35,
        "J": 40,
    }

    for coluna, largura in larguras_funcionarios.items():
        ws_funcionarios.column_dimensions[coluna].width = largura

    larguras_contas = {
        "A": 20,
        "B": 30,
        "C": 15,
        "D": 15,
        "E": 20,
        "F": 15,
        "G": 20,
        "H": 25,
        "I": 35,
        "J": 15,
        "K": 40,
    }

    for coluna, largura in larguras_contas.items():
        ws_contas.column_dimensions[coluna].width = largura

    for ws in [ws_funcionarios, ws_contas]:
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions

    # Formatação de datas
    for linha in range(2, 1002):
        ws_funcionarios.cell(
            row=linha,
            column=6,
        ).number_format = "dd/mm/yyyy"

    # ==========================================================
    # INSTRUÇÕES
    # ==========================================================

    ws_funcionarios["L1"] = "INSTRUÇÕES"
    ws_funcionarios["L1"].font = Font(bold=True)

    ws_funcionarios["L2"] = "Preencha uma linha para cada funcionário."

    ws_funcionarios["L3"] = "Empresa é obrigatória."

    ws_funcionarios["L4"] = "Função pode ficar em branco."

    ws_funcionarios["L5"] = "O CPF deve possuir 11 dígitos."

    ws_funcionarios["L6"] = "A aba ContasBancarias é opcional."

    ws_contas["M1"] = "INSTRUÇÕES"
    ws_contas["M1"].font = Font(bold=True)

    ws_contas["M2"] = "Use o CPF para vincular a conta ao funcionário."

    ws_contas["M3"] = "Se não houver conta bancária, não informe nada nesta aba."

    ws_contas["M4"] = "Todos os campos bancários obrigatórios devem ser preenchidos."

    ws_contas["M5"] = "Somente uma conta por funcionário pode ser marcada como padrão."

    # Oculta a aba de listas
    ws_listas.sheet_state = "hidden"

    # ==========================================================
    # RETORNO
    # ==========================================================

    arquivo = BytesIO()

    workbook.save(arquivo)

    arquivo.seek(0)

    return arquivo
