"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect


from . import index
from webapp.views import login_view, registrar_curso, lista_funcionarios, pagina_inicial, detalhes_funcionario, buscar_nome_funcionario

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('', index.index),
    path('', lambda request: redirect('login/')),
    path('login/', login_view, name='login'),
    path('cursos/', registrar_curso, name='cursos'),
    path('buscar_nome_funcionario/', buscar_nome_funcionario, name='buscar_nome_funcionario'),
    path('funcionarios/detalhes_funcionario/<str:funcionario_id>/', detalhes_funcionario, name='detalhes_funcionario'),
    path('pagina_inicial/', pagina_inicial, name='pagina_inicial'),
    path('funcionarios/', lista_funcionarios, name='lista_funcionarios'),
]
