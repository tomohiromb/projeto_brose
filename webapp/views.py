import json
import csv
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .models import Funcionario, Login, Skills, Cargo
from .forms import LoginForm, FuncionarioSearchForm, CursosForm, LoginFormCreate, SkillFormCreate, FuncionarioFormCreate, CargoFormCreate
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

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

                    # login(request, user)  # Garante que o usuário está autenticado
                    # Redireciona para a página inicial
                    return redirect(request.GET.get('next') or 'pagina_inicial')
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
            resultados = resultados.filter(
                cargo__departamento__icontains=setor)

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
            resultados = resultados.filter(
                cargo__nome_do_cargo__icontains=descricao)

        ultima_verificacao = form.cleaned_data.get('ultima_verificacao')
        if ultima_verificacao:
            resultados = resultados.filter(
                ultima_verificacao__icontains=ultima_verificacao)

    else:
        print(form.errors)
    context = {
        'form': form,
        'resultados': resultados,
    }

    return render(request, 'funcionarios.html', context)

def detalhes_funcionario(request, funcionario_id,cargo_id):
    # Busca o funcionário pelo ID, ou retorna 404 se não encontrado
    funcionario = get_object_or_404(Funcionario, id=funcionario_id)
    cargo = get_object_or_404(Cargo, id=cargo_id)
    # Verifique se funcionario.skills é uma string ou uma lista
    if isinstance(funcionario.skills, str):
        # Converter a string de skills de JSON para lista de dicionários
        try:
            skills_list = json.loads(
                funcionario.skills) if funcionario.skills else []
            skills_list = json.loads(
                funcionario.skills) if funcionario.skills else []
        except json.JSONDecodeError:
            skills_list = []
    elif isinstance(funcionario.skills, list):
        # Se já for uma lista, atribua diretamente
        skills_list = funcionario.skills
    else:
        # Caso contrário, atribua uma lista vazia
        skills_list = []
    skills_list_dict = {
            skill['nome_skill']: skill['nivel'] for skill in skills_list
        }
    
    if isinstance(cargo.skills, str):
        # Converter a string de skills de JSON para lista de dicionários
        try:
            skills_cargo = json.loads(
                cargo.skills) if cargo.skills else []
        except json.JSONDecodeError:
            skills_cargo = []
    elif isinstance(cargo.skills, list):
        # Se já for uma lista, atribua diretamente
        skills_cargo = cargo.skills
    else:
        # Caso contrário, atribua uma lista vazia
        skills_cargo = []
    skills_cargo_dict = {
            skill['nome_skill']: skill['nivel'] for skill in skills_cargo
        }
    
    # Comparar as skills
    comparacoes = []
    for nome_skill, nivel_cargo in skills_cargo_dict.items():
        nivel_funcionario = skills_list_dict.get(nome_skill)
        if nivel_funcionario is not None:
            if nivel_funcionario > nivel_cargo:
                status = "up"  # Representa seta para cima
            elif nivel_funcionario == nivel_cargo:
                status = "equal"  # Representa igualdade
            else:
                status = "down"  # Representa seta para baixo
        else:
            nivel_funcionario = "N/A" 
            status = None  # Skill ausente no funcionário
            
        comparacoes.append({
            "nome_skill": nome_skill,
            "nivel_funcionario": nivel_funcionario,
            "nivel_cargo": nivel_cargo,
            "status": status
        })
    # Monta os dados para o JSON de resposta
    dados_funcionario = {
        'id': funcionario.id,
        'nome': funcionario.nome_funcionario,
        'cargo': funcionario.cargo_id,
        'departamento': funcionario.cargo.departamento if funcionario.cargo else '',
        'descricao': funcionario.cargo.nome_do_cargo if funcionario.cargo else '',
        'skills': skills_list,
        'comparacoes': comparacoes 
    }

    return JsonResponse(dados_funcionario)  # Retorna os dados em JSON

def listar_cargos(request):
    # Buscar todos os cargos
    cargos = Cargo.objects.all()

    cargos_list = []
    for cargo in cargos:
        # Parsear as skills necessárias do JSON
        try:
            # Parseando o JSON de skills
            skills_list = json.loads(cargo.skills)
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


def buscar_nome_funcionario(request):
    funcionario_id = request.GET.get('id')
    try:
        funcionario = Funcionario.objects.get(id=funcionario_id)
        # Supondo que o campo de nome seja 'nome'
        return JsonResponse({'nome': funcionario.nome_funcionario})
    except Funcionario.DoesNotExist:
        return JsonResponse({'nome': ''})  # Retorna vazio se não encontrar


def buscar_skills(request):
    if request.method == "GET":
        skills = Skills.objects.values('id', 'nome_skill')
        skill_list = [skill['nome_skill'] for skill in skills]
        return JsonResponse(skill_list, safe=False)


def gerenciar_registros(request):
    # Inicializar formulários
    skill_form = SkillFormCreate(prefix='skill')
    funcionario_form = FuncionarioFormCreate(prefix='funcionario')
    cargo_form = CargoFormCreate(prefix='cargo')
    login_form = LoginFormCreate(prefix='login')

    if request.method == 'POST':
        # Verificar qual formulário de criação foi enviado
        if 'submit_skill' in request.POST:
            skill_form = SkillFormCreate(request.POST, prefix='skill')
            if skill_form.is_valid():
                skill_form.save()
                return redirect('gerenciar_registros')

        elif 'submit_funcionario' in request.POST:
            funcionario_form = FuncionarioFormCreate(request.POST, prefix='funcionario')
            if funcionario_form.is_valid():
                funcionario = funcionario_form.save(commit=False)
                funcionario.save()
                return redirect('gerenciar_registros')

        elif 'submit_cargo' in request.POST:
            cargo_form = CargoFormCreate(request.POST, prefix='cargo')
            if cargo_form.is_valid():
                cargo = cargo_form.save(commit=False)
                cargo.skills = cargo_form.cleaned_data.get('skills') or '[]'
                cargo.save()
                return redirect('gerenciar_registros')

        elif 'submit_login' in request.POST:
            login_form = LoginFormCreate(request.POST, prefix='login')
            if login_form.is_valid():
                login_form.save()
                return redirect('gerenciar_registros')

        # Verificar qual exclusão foi solicitada
        elif 'delete_skill' in request.POST:
            skill_id = request.POST.get('skill')
            skill = get_object_or_404(Skills, id=skill_id)
            skill.delete()
            return redirect('gerenciar_registros')

        elif 'delete_funcionario' in request.POST:
            funcionario_id = request.POST.get('funcionario')
            funcionario = get_object_or_404(Funcionario, id=funcionario_id)
            funcionario.delete()
            return redirect('gerenciar_registros')

        elif 'delete_cargo' in request.POST:
            cargo_id = request.POST.get('cargo')
            cargo = get_object_or_404(Cargo, id=cargo_id)
            cargo.delete()
            return redirect('gerenciar_registros')

        elif 'delete_login' in request.POST:
            login_id = request.POST.get('login')
            login = get_object_or_404(Login, id=login_id)
            login.delete()
            return redirect('gerenciar_registros')

    # Obter os registros existentes
    # skills = Skills.objects.all()
    # funcionarios = Funcionario.objects.all()
    # cargos = Cargo.objects.all()
    # logins = Login.objects.all()

    return render(request, 'gerenciar_registros.html', {
        'skill_form': skill_form,
        'funcionario_form': funcionario_form,
        'cargo_form': cargo_form,
        'login_form': login_form,
    #    'skills': skills,
    #    'funcionarios': funcionarios,
    #    'cargos': cargos,
    #    'logins': logins,
    })

def exportar_csv(request):
    # Configurar a resposta como CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="funcionarios.csv"'

    # Criar o writer com delimitador personalizado
    # Alterado para ponto-e-vírgula
    writer = csv.writer(response, delimiter=';')

    # Escrever o cabeçalho do CSV
    writer.writerow(['ID', 'Nome', 'Cargo', 'Skills',
                    'Certificados', 'Última Verificação'])

    # Escrever os dados dos funcionários
    funcionarios = Funcionario.objects.all()
    for funcionario in funcionarios:
        writer.writerow([
            funcionario.id,
            funcionario.nome_funcionario,
            funcionario.cargo.nome_do_cargo,  # Acessando o nome do cargo relacionado
            funcionario.skills,
            funcionario.certificados,
            funcionario.ultima_verificacao,
        ])

    return response

def exportar_pdf(request):
    # Cria um response HTTP com o tipo de conteúdo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'

    # Configura o tamanho da página e cria o canvas
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Adiciona título ao PDF
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "Relatório de Dados")
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 70, "Dados extraídos do banco de dados")

    # Configura o espaço inicial para os dados
    y = height - 100

    # Busca os dados no banco de dados
    registros = Funcionario.objects.all()  # Ajuste de acordo com o seu modelo

    # Cria uma tabela básica com os dados
    for registro in registros:
        if y < 50:  # Se a página estiver cheia, cria uma nova página
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 12)

        # Escreve as informações no PDF
        p.drawString(100, y, f"ID: {registro.id} | Nome: {registro.nome_funcionario} | Cargo: {registro.cargo.nome_do_cargo} | Skills: {registro.skills} | Certificados: {registro.certificados} | Última Verificação: {registro.ultima_verificacao}")

        y -= 20

    # Finaliza o PDF
    p.showPage()
    p.save()

    return response

#@login_required   
def pagina_inicial(request):
    return render(request, 'inicio.html')

#def funcionarios(request):
 #   return render(request, 'funcionarios.html')