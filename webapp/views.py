from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Login
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        
        # Instancia o formulário com os dados enviados pelo usuário (request.POST)
        form = LoginForm(request.POST)
        
        # Verifica se o formulário é válido (se todos os campos foram preenchidos corretamente)
        if form.is_valid():
            login = form.cleaned_data.get('login')
            senha = form.cleaned_data.get('senha')
            
            # Tentativa de buscar o usuário pelo login fornecido
            try:
                user = Login.objects.get(login=login)
                
                # Verifica se a senha inserida é a mesma cadastrada no banco de dados
                if user.verify_password(senha):
                    messages.success(request, 'Login bem-sucedido!')
                else:
                    messages.error(request, 'Senha incorreta.')
                    
            # Caso o Usuário não exista
            except Login.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
                
    # Se o método da requisição não for POST (por exemplo, GET), uma nova instância do formulário é criada
    else:
        form = LoginForm()

    # Renderiza a página de login com o formulário (seja preenchido ou vazio)
    return render(request, 'login.html', {'form': form})
