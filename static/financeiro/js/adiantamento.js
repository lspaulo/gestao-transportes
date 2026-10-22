
document.addEventListener("DOMContentLoaded", () => {
    const funcionario = document.getElementById("id_funcionario");
    const conta = document.getElementById("id_conta_bancaria");
    const empresa = document.getElementById("id_empresa");
    const cpf = document.getElementById("id_cpf");

    if (!funcionario) return;

    async function carregarDadosFuncionario() {
        if (!funcionario.value) {
            conta.innerHTML = "";
            empresa.value = "";
            cpf.value = "";
            return;
        }

        try {
            const urlBase = funcionario.dataset.url;

            const response = await fetch(
                `${urlBase}${funcionario.value}/contas/`
            );

            if (!response.ok) {
                throw new Error("Não foi possível carregar os dados do motorista.");
            }

            const dados = await response.json();

            empresa.value = dados.empresa.nome || "";
            cpf.value = dados.funcionario.cpf || "";

            // Preserva a conta selecionada na edição.
            const contaSelecionada = conta.value;

            conta.innerHTML = "";

            dados.contas.forEach((item) => {
                const option = document.createElement("option");

                option.value = item.id;
                option.text = `${item.banco} - ${item.numero}-${item.digito}`;

                conta.appendChild(option);
            });

            if (
                contaSelecionada &&
                dados.contas.some(
                    (item) => String(item.id) === String(contaSelecionada)
                )
            ) {
                conta.value = contaSelecionada;
            } else if (dados.conta_padrao !== null) {
                conta.value = String(dados.conta_padrao);
            }
        } catch (erro) {
            console.error("Erro ao carregar dados do motorista:", erro);
        }
    }

    funcionario.addEventListener("change", carregarDadosFuncionario);

    // Carrega também ao abrir um formulário de edição.
    carregarDadosFuncionario();
});
