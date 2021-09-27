from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from .models import Beneficiario
from django import template

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, 'polls/principal.html')


def cruzamento(request):
    return render(request, 'polls/cruzamento_beneficiario.html')


def cruzar(request):
    if request.method == "POST":
        nome = request.POST.get('nomeBeneficiario')
        return render(request, 'polls/cruzamento_beneficiario.html', {'data': nome}),
    else:
        return redirect('cruzamento')


class BeneficiarioListView(ListView):
    model = Beneficiario


class BeneficiarioDetailView(DetailView):
    model = Beneficiario
