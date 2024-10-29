from django import forms
from .models import Funcionario, Skills, Cursos

class LoginForm(forms.Form):
    # Campo de texto para o login, com um comprimento máximo de 150 caracteres
    # O widget TextInput é usado para customizar a aparência do campo, com um placeholder 'login'
    login = forms.CharField(
        max_length=100,
        label='Usuário',
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu usuário'})
    )
    
    # Campo de senha, usando o widget PasswordInput para garantir que os caracteres digitados fiquem ocultos (tipo "password")
    # O placeholder 'senha' é exibido como dica dentro do campo
    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'}))

class FuncionarioSearchForm(forms.Form):
    
    id_funcionario = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Digite o id do funcionário para filtrar...'}))
    
    nome = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Digite o nome do funcionário para filtrar...'}))
    
    skill = forms.ModelChoiceField(queryset=Skills.objects.all(), required=False, empty_label='Selecione uma skill para filtrar...',
                                   widget=forms.Select(attrs={'class': 'labels'}))
    
    setor = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Digite o setor para filtrar...'}))
    
    posicao = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Digite a posição para filtrar...'}))
    
    descricao = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Digite a descrição para filtrar...'}))
    
    ultima_verificacao = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    
class CursosForm(forms.ModelForm):
    funcionario_id = forms.CharField(
    widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'funcionario-id', 'placeholder' : 'Digite o id do funcionário'})
    )
    
    nome_skill = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'nome_do_funcionario', 'placeholder' : 'Digite o nome da skill'})
    )
    
    data_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    data_termino = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Cursos
        fields = ['funcionario_id', 'nome_skill', 'data_inicio', 'data_termino']