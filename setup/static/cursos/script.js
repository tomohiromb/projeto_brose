document.getElementById('funcionario_id').addEventListener('blur', function() {
    const id = this.value;

    // Faz a requisição para a view de autocompletar
    fetch(`buscar_nome_funcionario/?id=${id}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                document.getElementById('nome_funcionario').value = '';  // Limpa o campo se houver erro
            } else {
                // Preenche o campo de nome_funcionario com o valor retornado
                document.getElementById('nome_funcionario').value = data.nome;
            }
        })
        .catch(error => console.error('Erro na requisição:', error));
});