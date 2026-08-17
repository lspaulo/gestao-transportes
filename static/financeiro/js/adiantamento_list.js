document.addEventListener(
    "DOMContentLoaded",
    () => {

        const checkboxes =
            document.querySelectorAll(
                ".selecionar-adiantamento"
            );

        const contador =
            document.getElementById(
                "contador-selecionados"
            );

        const botao =
            document.getElementById(
                "btn-gerar-pdfs"
            );

        function atualizar() {

            const selecionados =
                document.querySelectorAll(
                    ".selecionar-adiantamento:checked"
                ).length;

            contador.textContent =
                `${selecionados} selecionados`;

            botao.disabled =
                selecionados === 0;

        }

        checkboxes.forEach((item) => {

            item.addEventListener(
                "change",
                atualizar,
            );

        });

    },
);