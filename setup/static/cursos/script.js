document.addEventListener("DOMContentLoaded", function () {
    // Seleciona todos os botões que abrem pop-ups
    const buttons = document.querySelectorAll(".form-group-buttom button");
    const popup = document.querySelector("#popup");
    const closeBtn = popup.querySelector(".close");
    const popupContent = popup.querySelector(".popup-content");

    // Conteúdos diferentes para cada botão
    const popupContents = {
        "adicionar-funcionario": `
            <h3>Adicionar Novo Funcionário</h3>
            <p>Preencha os campos para adicionar um novo funcionário.</p>
            <form>
                <label for="nome_funcionario">Nome do funncionário</label>

                <input type="text" id="nome_funcionario">

                <label for="id">Id do Funcionário</label>

                <input type="text" id="id" name="id">

                <label for="cargo">Cargo do funcionário</label>

                <input type="text" id="cargo">

                <button type="submit">Salvar</button>
            </form>`,

        "adicionar-skill": `

            <h3>Adicionar Nova Skill</h3>

            <p>Informe os detalhes da nova habilidade.</p>

            <form>

                <label for="id_skill">Id da skill</label>

                <input type="text" id="id_skill">

                <label for="nome_skill">Nome da skill</label>

                <input type="text" id="nome_skill">

                <button type="submit">Adicionar</button>

            </form>`,

        "inativar-funcionario": `

            <h3>Inativar Funcionário</h3>

            <p>Digite o id do funcionário para inativar.</p>

            <form>

                <label for="ID_employee">Id do funcionário</label>

                <input type="text" id="id_employee">

                <button type="submit">Inativar</button>

            </form>`,
        "deletar-skill": `

            <h3>Deletar Skill</h3>

            <p>Digite o ID skill que deseja deletar.</p>

            <form>
                <label for="id_skill">ID Skill</label>

                <input type="text" id="id_skill">

                <button type="submit">Deletar</button>
            </form>`
    };

    // Adiciona eventos de clique para abrir o pop-up com conteúdo correspondente
    buttons.forEach(button => {
        button.addEventListener("click", function () {
            const id = button.id;
            if (popupContents[id]) {
                popupContent.innerHTML = popupContents[id];
                popup.style.display = "flex"; // Exibe o pop-up
            }
        });
    });

    // Fecha o pop-up quando o botão de fechar é clicado
    closeBtn.addEventListener("click", function () {
        popup.style.display = "none";
    });

    // Fecha o pop-up se clicar fora do conteúdo
    window.addEventListener("click", function (event) {
        if (event.target === popup) {
            popup.style.display = "none";
        }
    });
});
