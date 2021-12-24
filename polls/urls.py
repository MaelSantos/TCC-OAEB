from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('cruzamento/auxilios/', views.cruzamento, name='cruzamento_auxilios'),
    path('cruzamento/auxilios/busca/', views.cruzar, name='cruzar_auxilios'),

    path('analise/', views.analise, name='denuncie'),
    path('contatos/', views.contatos, name='contatos'),

    path('cruzamento/salvar/pdf/', views.gerar_pdf, name='salvar_pdf'),
    path('cruzamento/salvar/csv/', views.gerar_csv, name='salvar_csv'),

]
