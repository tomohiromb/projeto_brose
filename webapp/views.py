import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Funcionario, Login, Skills
from .forms import LoginForm, FuncionarioSearchForm, CursosForm
from .models import Cargo

def login_view(request):
    if request.method == 'POST':
        
        # Instancia o formulário com os dados enviados pelo usuário (request.POST)
        form = LoginForm(request.POST)
        
        # Verifica se o formulário é válido (se todos os campos foram preenchidos corretamente)
        if form.is_valid():
            login_name = form.cleaned_data.get('login')
            senha = form.cleaned_data.get('senha')
            
            # Tentativa de buscar o usuário pelo login fornecido
            try:
                user = Login.objects.get(login=login_name)
                
                # Verifica se a senha inserida é a mesma cadastrada no banco de dados
                if user.verify_password(senha):
                    
                    #login(request, user)  # Garante que o usuário está autenticado
                    return redirect(request.GET.get('next') or 'pagina_inicial')  # Redireciona para a página inicial
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

def lista_funcionarios(request):
    form = FuncionarioSearchForm(request.GET or None)
    resultados = Funcionario.objects.all()

    if form.is_valid():

        # Filtro por ID do Funcionário
        id_funcionario = form.cleaned_data.get('id_funcionario')
        if id_funcionario:
            resultados = resultados.filter(id=id_funcionario)
        
        # Filtro por nome
        nome = form.cleaned_data.get('nome')   
        if nome:
            resultados = resultados.filter(nome_funcionario__icontains=nome)

        # Filtro por setor
        setor = form.cleaned_data.get('setor')
        if setor:
            resultados = resultados.filter(cargo__departamento__icontains=setor)

        # Filtro por skill
        skill = form.cleaned_data.get('skill')
        if skill:
            resultados = resultados.filter(skills__icontains=skill)
        
        # Filtro por posição
        posicao = form.cleaned_data.get('posicao')
        if posicao:
            resultados = resultados.filter(cargo__id__icontains=posicao)

        # Filtro por descrição
        descricao = form.cleaned_data.get('descricao')
        if descricao:
            resultados = resultados.filter(cargo__nome_do_cargo__icontains=descricao)
            
        ultima_verificacao = form.cleaned_data.get('ultima_verificacao')
        if ultima_verificacao:
            resultados = resultados.filter(ultima_verificacao__icontains=ultima_verificacao)
    
    else:
        print(form.errors)
    context = {
        'form': form,
        'resultados': resultados,
    }
    
    return render(request, 'funcionarios.html', context)

def detalhes_funcionario(request, funcionario_id):
    # Busca o funcionário pelo ID, ou retorna 404 se não encontrado
    funcionario = get_object_or_404(Funcionario, id=funcionario_id)

    # Verifique se funcionario.skills é uma string ou uma lista
    if isinstance(funcionario.skills, str):
        # Converter a string de skills de JSON para lista de dicionários
        try:
            skills_list = json.loads(funcionario.skills) if funcionario.skills else []
        except json.JSONDecodeError:
            skills_list = []
    elif isinstance(funcionario.skills, list):
        # Se já for uma lista, atribua diretamente
        skills_list = funcionario.skills
    else:
        # Caso contrário, atribua uma lista vazia
        skills_list = []

    # Monta os dados para o JSON de resposta
    dados_funcionario = {
        'id': funcionario.id,
        'nome': funcionario.nome_funcionario,
        'cargo': funcionario.cargo_id,
        'departamento': funcionario.cargo.departamento if funcionario.cargo else '',
        'descricao': funcionario.cargo.nome_do_cargo if funcionario.cargo else '',
        'skills': skills_list,
    }

    return JsonResponse(dados_funcionario)  # Retorna os dados em JSON


def listar_cargos(request):
    # Buscar todos os cargos
    cargos = Cargo.objects.all()
    
    cargos_list = []
    for cargo in cargos:
        # Parsear as skills necessárias do JSON
        try:
            skills_list = json.loads(cargo.skills)  # Parseando o JSON de skills
        except json.JSONDecodeError:
            skills_list = []  # Caso o JSON esteja inválido ou vazio
        
        cargos_list.append({
            'cargo': cargo,
            'skills': skills_list
        })

    context = {
        'cargos_list': cargos_list
    }

    return render(request, 'listar_cargos.html', context)

def registrar_curso(request):
    if request.method == 'POST':
        form = CursosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso registrado com sucesso!')
    else:
        form = CursosForm()
    
    return render(request, 'cursos.html', {'form': form})

# API para autocomplete de skills
def autocomplete_skill(request):
    if request.is_ajax():
        query = request.GET.get('term', '')
        # Supondo que as skills estão armazenadas no campo 'skills' em Funcionario
        skills = Funcionario.objects.values_list('skills', flat=True)
        
        # Agrupar todas as skills e remover duplicatas
        skills_list = set()
        for skill_json in skills:
            try:
                skill_data = json.loads(skill_json)
                for skill in skill_data:
                    if query.lower() in skill['nome_skill'].lower():
                        skills_list.add(skill['nome_skill'])
            except json.JSONDecodeError:
                continue
        
        # Retornar as skills que combinam com o termo de pesquisa
        return JsonResponse(list(skills_list), safe=False)

def buscar_nome_funcionario(request):
    funcionario_id = request.GET.get('id')
    try:
        funcionario = Funcionario.objects.get(id=funcionario_id)
        return JsonResponse({'nome': funcionario.nome_funcionario})  # Supondo que o campo de nome seja 'nome'
    except Funcionario.DoesNotExist:
        return JsonResponse({'nome': ''})  # Retorna vazio se não encontrar

#@login_required   
def pagina_inicial(request):
    return render(request, 'inicio.html')

def funcionarios(request):
    return render(request, 'funcionarios.html')