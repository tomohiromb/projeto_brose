from django.db import models

class Login(models.Model):
    
    # Campo para o login do usuário, com um máximo de 250 caracteres e garantindo que seja único no banco de dados
    login = models.CharField(max_length=250, unique=True)
    
    # Campo para armazenar a senha do usuário, com um máximo de 30 caracteres
    senha = models.CharField(max_length=30)
    
     # Método para verificar se a senha fornecida é igual à senha armazenada
    def verify_password(self, tentativa_senha):
        
        # Se a senha fornecida for igual à senha do usuário no banco de dados, retorna True
        if self.senha == tentativa_senha:
            return True
        else:
            return False
    
    # Método especial que retorna uma representação em string do objeto (neste caso, o login)
    def __str__(self):
        return self.login