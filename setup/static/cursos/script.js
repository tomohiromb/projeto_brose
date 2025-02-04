document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".form-group-buttom button");
    const popup = document.querySelector("#popup");
    const closeBtn = popup.querySelector(".close");
    const forms = {
        "adicionar-skill": "form-skill",
        "adicionar-funcionario": "form-funcionario",
        "adicionar-cargo": "form-cargo",
        "adicionar-login": "form-login",
    };

    // Mostrar o formulário correto no pop-up
    buttons.forEach(button => {
        button.addEventListener("click", function () {
            const formId = forms[button.id];
            if (formId) {
                document.querySelectorAll("#popup form").forEach(form => form.style.display = "none");
                const selectedForm = document.querySelector(`#${formId}`);
                selectedForm.style.display = "block";
                popup.style.display = "flex";
            }
        });
    });

    // Fechar o pop-up
    closeBtn.addEventListener("click", function () {
        popup.style.display = "none";
    });

    // Fechar o pop-up clicando fora
    window.addEventListener("click", function (event) {
        if (event.target === popup) {
            popup.style.display = "none";
        }
    });
});

