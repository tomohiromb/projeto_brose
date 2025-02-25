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
from django.contrib import admin
from django.urls import path, include



from . import index
from webapp.views import (
    login_view,
    registrar_curso,
    lista_funcionarios,
    pagina_inicial,
    detalhes_funcionario,
    buscar_nome_funcionario,
    buscar_skills,
    gerenciar_registros,
    exportar_csv,
    exportar_pdf
)

urlpatterns = [
    #path('admin/', admin.site.urls),exportar_csv
    #path('', index.index),
    path('', lambda request: redirect('login/')),
    path('login/', login_view, name='login'),
    path('cursos/', registrar_curso, name='cursos'),
    path('buscar_nome_funcionario/', buscar_nome_funcionario, name='buscar_nome_funcionario'),
    path('funcionarios/detalhes_funcionario/<str:funcionario_id>/<str:cargo_id>/', detalhes_funcionario, name='detalhes_funcionario'),
    path('funcionarios/buscar_skills/', buscar_skills, name='buscar_skills'),
    path('pagina_inicial/', pagina_inicial, name='pagina_inicial'),
    path('funcionarios/', lista_funcionarios, name='lista_funcionarios'),
    path('gerenciar_registros/', gerenciar_registros, name='gerenciar_registros'),
    path('exportar-csv/', exportar_csv, name='exportar_csv'),
    path('exportar-pdf/', exportar_pdf, name='exportar_pdf')
]
