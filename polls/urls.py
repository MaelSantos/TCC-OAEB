from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('beneficiarios/', views.busca, name='busca'),
    path('beneficiarios/buscar/', views.buscar, name='buscar'),
    path('bolsa-familia/', views.bolsa_famila, name='bolsa_familia'),
    path('bolsa-familia/beneficiarios/', views.buscar_bolsa_famila, name='busca_bolsa_familia'),

    path('cruzamento/auxilios/', views.cruzamento, name='cruzamento_auxilios'),
    path('cruzamento/auxilios/busca/', views.cruzar, name='cruzar_auxilios'),

]
