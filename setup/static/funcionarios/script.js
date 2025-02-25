document.addEventListener("DOMContentLoaded", function() {
    // Seleciona todos os botões "Editar"
    const editButtons = document.querySelectorAll(".editar-botao");
    const popup = document.querySelector(".popup");
    const closeBtn = document.querySelector(".close");

    // Função para buscar dados do funcionário pelo ID e preencher o popup

    
    function CarregarDetalhesFuncionario(funcionarioId, cargoId) {
        
        const url = `/funcionarios/detalhes_funcionario/${funcionarioId}/${cargoId}/`;
        console.log("URL:", url);
        console.log('funcionarioId:', funcionarioId);
        console.log('Cargo ID:', cargoId)
        document.getElementById("popup").style.display = "block";
        fetch(url)  // Ajuste essa URL para corresponder à sua URL de detalhes
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
                
                // Preencher as comparações com setas ao lado de cada skill
                const comparacoesDiv = document.getElementById('comparacoes');
                if (data.comparacoes.length > 0) {
                    comparacoesDiv.innerHTML = data.comparacoes
                        .map(comparacao => {
                            let seta = '';
                            if (comparacao.status === "up") {
                                seta = `<span style="color: green;">&#9650;</span>`; // Seta para cima
                            } else if (comparacao.status === "down") {
                                seta = `<span style="color: red;">&#9660;</span>`; // Seta para baixo
                            } else {
                                seta = ''; // Caso não haja status
                            }
                            return `${comparacao.nome_skill}: ${comparacao.nivel_funcionario} vs ${comparacao.nivel_cargo} ${seta}`;
                        })
                        .join('<br>');  // Para separar as comparações por linha
                } else {
                    comparacoesDiv.innerHTML = "Sem comparações disponíveis";
                }
                
                // Exibir o popup
                popup.style.display = "flex"; // Use "flex" para centralizar o conteúdo
            })
            .catch(error => console.error('Erro ao buscar os detalhes do funcionário:', error));
    }

    function carregarSkills(callback) {
        fetch('buscar_skills/')
            .then(response => response.json())
            .then(data => {
                callback(data); // Chama o autocomplete com a lista de skills
            })
            .catch(error => console.error('Erro ao carregar skills:', error));
    }

    // Função de autocomplete com lista dinâmica de skills
    function autocomplete(inp, arr) {
        var currentFocus;

        inp.addEventListener("input", function (e) {
            var a, b, i, val = this.value;
            closeAllLists();
            if (!val) return false;
            currentFocus = -1;

            a = document.createElement("DIV");
            a.setAttribute("id", this.id + "autocomplete-list");
            a.setAttribute("class", "autocomplete-items");
            this.parentNode.appendChild(a);

            for (i = 0; i < arr.length; i++) {
                if (arr[i].substr(0, val.length).toUpperCase() === val.toUpperCase()) {
                    b = document.createElement("DIV");
                    b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                    b.innerHTML += arr[i].substr(val.length);
                    b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                    b.addEventListener("click", function (e) {
                        inp.value = this.getElementsByTagName("input")[0].value;
                        closeAllLists();
                    });
                    a.appendChild(b);
                }
            }
        });

        inp.addEventListener("keydown", function (e) {
            var x = document.getElementById(this.id + "autocomplete-list");
            if (x) x = x.getElementsByTagName("div");
            if (e.keyCode === 40) {
                currentFocus++;
                addActive(x);
            } else if (e.keyCode === 38) {
                currentFocus--;
                addActive(x);
            } else if (e.keyCode === 13) {
                e.preventDefault();
                if (currentFocus > -1) {
                    if (x) x[currentFocus].click();
                }
            }
        });

        function addActive(x) {
            if (!x) return false;
            removeActive(x);
            if (currentFocus >= x.length) currentFocus = 0;
            if (currentFocus < 0) currentFocus = x.length - 1;
            x[currentFocus].classList.add("autocomplete-active");
        }

        function removeActive(x) {
            for (var i = 0; i < x.length; i++) {
                x[i].classList.remove("autocomplete-active");
            }
        }

        function closeAllLists(elmnt) {
            var x = document.getElementsByClassName("autocomplete-items");
            for (var i = 0; i < x.length; i++) {
                if (elmnt !== x[i] && elmnt !== inp) {
                    x[i].parentNode.removeChild(x[i]);
                }
            }
        }

        document.addEventListener("click", function (e) {
            closeAllLists(e.target);
        });
    }

    // Inicializa o autocomplete após carregar as skills
    carregarSkills(function (skills) {
        autocomplete(document.getElementById("myInput"), skills);  // Substitua "myInput" pelo ID do seu campo
    });

    // Adiciona um evento de clique para cada botão "Editar"
    editButtons.forEach(button => {
        button.addEventListener("click", function() {

            const funcionarioId = this.dataset.funcionarioId; // Supondo que você armazene o ID no botão
            const cargoId = this.dataset.cargoId; // ID do cargo
            console.log("Funcionário ID:", funcionarioId); 
            console.log("Cargo ID:", cargoId);
            CarregarDetalhesFuncionario(funcionarioId,cargoId); // Chama a função para carregar os dados do funcionário
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

// Adiciona evento de clique nos itens do drop-down
dropdown.addEventListener('click', (event) => {
    if (event.target.tagName === 'A') {
        event.preventDefault();
        searchInput.value = event.target.textContent; // Atualiza o input com o valor clicado
        dropdown.style.display = 'none'; // Esconde o dropdown após seleção
    }
});

