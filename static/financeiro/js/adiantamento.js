document.addEventListener("DOMContentLoaded", () => {

    const funcionario = document.getElementById("id_funcionario");
    const conta = document.getElementById("id_conta_bancaria");
    const empresa = document.getElementById("id_empresa");

    if (!funcionario) {
        return;
    }

    funcionario.addEventListener("change", async () => {

        conta.innerHTML = "";
        empresa.value = "";

        if (!funcionario.value) {
            return;
        }

        try {

            const urlBase = funcionario.dataset.url;

            const response = await fetch(
                `${urlBase}${funcionario.value}/contas/`
            );

            const dados = await response.json();

            empresa.value = dados.empresa.nome;
            console.log(dados);

            dados.contas.forEach((item) => {

                const option = document.createElement("option");

                option.value = item.id;

                option.text =
                    `${item.banco} - ${item.numero}-${item.digito}`;

                if (item.id === dados.conta_padrao) {
                    option.selected = true;
                }

                conta.appendChild(option);

            });

        } catch (erro) {

            console.error(erro);

        }

    });

});