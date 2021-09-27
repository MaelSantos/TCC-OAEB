from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cruzamento/', views.cruzamento, name='cruzamento'),
    # path('', views.BeneficiarioListView.as_view(), name='BeneficiarioList'),
    # path("<slug:slug>/", views.BeneficiarioDetailView.as_view(), name='BeneficiarioDetail')
]
