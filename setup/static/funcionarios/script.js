document.addEventListener("DOMContentLoaded", function() {
    // Seleciona todos os botões "Editar"
    const editButtons = document.querySelectorAll(".editar-botao");
    const popup = document.querySelector(".popup");
    const closeBtn = document.querySelector(".close");

    // Função para buscar dados do funcionário pelo ID e preencher o popup

    
    function carregarDetalhesFuncionario(funcionarioId) {
        
        fetch(`detalhes_funcionario/${funcionarioId}/`)  // Ajuste essa URL para corresponder à sua URL de detalhes
            .then(response => response.json())
            .then(data => {
                console.log("Dados recebidos:", data);
                document.getElementById('posicao').value = data.cargo;
                document.getElementById('employee').value = data.id;
                document.getElementById('nome').value = data.nome;
                document.getElementById('setor').value = data.departamento;
                document.getElementById('descricao').value = data.descricao;
                
                // Preencher as skills
                const skillsTextarea = document.getElementById('skills');
                if (data.skills.length > 0) {
                    skillsTextarea.value = data.skills
                        .map(skill => `${skill.nome_skill} (Nível: ${skill.nivel})`)
                        .join('\n');
                } else {
                    skillsTextarea.value = "Nenhuma skill registrada";
                }
                
                // Exibir o popup
                popup.style.display = "flex"; // Use "flex" para centralizar o conteúdo
            })
            .catch(error => console.error('Erro ao buscar os detalhes do funcionário:', error));
    }

    // Adiciona um evento de clique para cada botão "Editar"
    editButtons.forEach(button => {
        button.addEventListener("click", function() {

            const funcionarioId = this.dataset.funcionarioId; // Supondo que você armazene o ID no botão
            console.log("Funcionário ID:", funcionarioId); 
            carregarDetalhesFuncionario(funcionarioId); // Chama a função para carregar os dados do funcionário
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
