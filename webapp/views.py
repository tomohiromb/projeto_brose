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


def lista_cargos(request):
    cargos = Cargo.objects.all()
    return render(request, 'lista_cargos.html', {'cargos': cargos})

def lista_funcionarios(request):
    
    form = FuncionarioSearchForm(request.GET or None)
    resultados = Funcionario.objects.all()

    if form.is_valid():
        
        # Filtro por nome
        nome = form.cleaned_data.get('nome')   
        if nome:
            resultados = resultados.filter(nome__icontains=nome)
            
        # Filtro por cargo/posição
        cargo = form.cleaned_data.get('cargo')
        if cargo:
            resultados = resultados.filter(cargo__icontains=cargo)

        # Filtro por setor
        setor = form.cleaned_data.get('setor')
        if setor:
            resultados = resultados.filter(setor__icontains=setor)

        # Filtro por skill
        skill = form.cleaned_data.get('skill')
        if skill:
            resultados = resultados.filter(funcionarioskill__skill=skill)
            
    context = {
    'form': form,
    'resultados': resultados,
    }
    
    return render(request, 'search_funcionarios.html', context)

def detalhes_funcionario(request, funcionario_id):
    # Busca o funcionário pelo ID, ou retorna 404 se não encontrado
    funcionario = get_object_or_404(Funcionario, id=funcionario_id)
    
    # Converter a string de skills de JSON para lista de dicionários
    try:
        skills_list = json.loads(funcionario.skills) if funcionario.skills else []
    except json.JSONDecodeError:
        skills_list = []
    
    # Converter a string de certificados de JSON para lista de dicionários
    try:
        certificados_list = json.loads(funcionario.certificados) if funcionario.certificados else []
    except json.JSONDecodeError:
        certificados_list = []

    context = {
        'funcionario': funcionario,
        'skills_list': skills_list,
        'certificados_list': certificados_list,
    }
    
    return render(request, 'detalhes_funcionario.html', context)

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
 
#@login_required   
def pagina_inicial(request):
    return render(request, 'inicio.html')

def cursos(request):
    return render(request, 'cursos.html')

def funcionarios(request):
    return render(request, 'funcionarios.html')