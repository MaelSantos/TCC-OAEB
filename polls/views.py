from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from .models import BeneficiarioAuxilio
from .crawler.crawler import Crawler
from django import template

# Create your views here.
from django.http import HttpResponse

crawler = Crawler()


def index(request):
    return render(request, 'polls/principal.html')


def cruzamento(request):
    return render(request, 'polls/cruzamento_beneficiario.html')


def cruzar(request):
    if request.method == "POST":
        nome = request.POST.get('nomeBeneficiario')

        # html = crawler.crawler_prefeitura('SantaCruz', nome)
        html = crawler.crawler_bolsafamilia()
        print(html)

        return render(request, 'polls/cruzamento_beneficiario.html', {'data': html, "nome": nome})
    else:
        return redirect('cruzamento')


class BeneficiarioListView(ListView):
    model = BeneficiarioAuxilio


class BeneficiarioDetailView(DetailView):
    model = BeneficiarioAuxilio
