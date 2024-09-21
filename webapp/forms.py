from django import forms

class LoginForm(forms.Form):
    # Campo de texto para o login, com um comprimento máximo de 150 caracteres
    # O widget TextInput é usado para customizar a aparência do campo, com um placeholder 'login'
    login = forms.CharField(
        max_length=150,
        label='Usuário',
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu usuário'})
    )
    
    # Campo de senha, usando o widget PasswordInput para garantir que os caracteres digitados fiquem ocultos (tipo "password")
    # O placeholder 'senha' é exibido como dica dentro do campo
    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'}))
