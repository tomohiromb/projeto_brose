from django.db import models

class Login(models.Model):
    
    id = models.BigAutoField(primary_key=True)
    
    login = models.CharField(unique=True, max_length=30)
    
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
    
    class Meta:
        managed = False
        db_table = 'webapp_login'
        

class Cargo(models.Model):
    
    id = models.CharField(primary_key=True, max_length=50)
    
    nome_do_cargo = models.CharField(max_length=100)
    
    departamento = models.CharField(max_length=100)
    
    skills = models.TextField(max_length=500)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'webapp_cargos'


class Funcionario(models.Model):
    
    id = models.CharField(primary_key=True, max_length=50)
    
    nome_funcionario = models.CharField(max_length=100)
	
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    
    skills = models.CharField(max_length=2000)
    
    certificados = models.TextField(max_length=2000)
    
    ultima_verificacao = models.DateField()

    class Meta:
        managed = False
        db_table = 'webapp_funcionarios'

class Skills(models.Model):
    
    id = models.CharField(primary_key=True, max_length=15)
    
    nome_skills = models.CharField(max_length=25)
    
    class Meta:
        managed = False
        db_table = 'webapp_skills'
        
class Cursos(models.Model):
    
    id = models.CharField(primary_key=True, max_length=15)
    
    funcionario_id = models.CharField(max_length=50)
    
    nome_skill = models.CharField(max_length=25)
    
    data_inicio = models.DateField()
    
    data_termino = models.DateField()
    
    class Meta:
        managed = False
        db_table = 'webapp_cursos'