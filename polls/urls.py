from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cruzamento/', views.cruzamento, name='cruzamento'),
    path('cruzamento/beneficiarios/', views.cruzar, name='cruzar'),
    path('bolsa-familia/', views.bolsa_famila, name='bolsa_familia'),
    path('bolsa-familia/beneficiarios/', views.cruzar_bolsa_famila, name='cruzar_bolsa_familia'),
    # path('', views.BeneficiarioListView.as_view(), name='BeneficiarioList'),
    # path("<slug:slug>/", views.BeneficiarioDetailView.as_view(), name='BeneficiarioDetail')
]
