document.addEventListener(
    "DOMContentLoaded",
    () => {

        const checkboxes =
            document.querySelectorAll(
                ".selecionar-adiantamento"
            );
        const selecionarTodos =
            document.getElementById(
                "selecionar-todos"
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
            selecionarTodos.checked =
                selecionados === checkboxes.length;

            contador.textContent =
                selecionados === 1
                    ? "1 selecionado"
                    : `${selecionados} selecionados`;

            botao.disabled =
                selecionados === 0;

        }

        checkboxes.forEach((item) => {

            item.addEventListener(
                "change",
                atualizar,
            );

        });
        if (selecionarTodos) {

            selecionarTodos.addEventListener(
                "change",
                function () {

                    checkboxes.forEach((item) => {

                        item.checked = this.checked;

                    });

                    atualizar();

                },
            );

        }

    },
);