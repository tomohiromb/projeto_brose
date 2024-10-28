document.addEventListener("DOMContentLoaded", function() {
    // Seleciona todos os botões "Editar"
    const editButtons = document.querySelectorAll(".editar-botao");
    const popup = document.querySelector(".popup");
    const closeBtn = document.querySelector(".close");

    // Adiciona um evento de clique para abrir o popup
    editButtons.forEach(button => {
        button.addEventListener("click", function() {
            popup.style.display = "flex"; // Use "flex" para centralizar o conteúdo
        });
    });

    // Fecha o popup quando o botão de fechar é clicado
    closeBtn.addEventListener("click", function() {
        popup.style.display = "none";
    });

    // Fecha o popup se clicar fora do conteúdo
    window.addEventListener("click", function(event) {
        if (event.target === popup) {
            popup.style.display = "none";
        }
    });
});
