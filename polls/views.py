from django.shortcuts import render, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .crawler.crawler import Crawler
from  .models import BeneficiarioAuxilio, BeneficiarioBolsaFamilia

crawler = Crawler()

engine = create_engine('mysql+pymysql://root:@localhost/teste?charset=utf8', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


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


def bolsa_famila(request):
    return render(request, "polls/bolsa_familia.html")


def cruzar_bolsa_famila(request):
    if request.method == "POST":
        nome = request.POST.get('nomeBeneficiario')
        nis = request.POST.get('nis')
        cpf = request.POST.get('cpf')

        # auxilio = BeneficiarioAuxilio.objects.filter(nome_beneficiario__icontains=nome)
        # bolsa = BeneficiarioBolsaFamilia.objects.filter(nome_favorecido__icontains=nome)

        # data = list(chain(auxilio, bolsa))
        # data = auxilio & bolsa

        # data = BeneficiarioAuxilio.objects.filter(nome_beneficiario__icontains=BeneficiarioBolsaFamilia.objects.filter(nome_favorecido__icontains=nome).values("nome_favorecido"))

        data = session.query(BeneficiarioAuxilio)
        print(data)

        return render(request, 'polls/bolsa_familia.html', {'data': data, "nome": nome, "nis": nis, "cpf": cpf})
    else:
        return redirect('cruzar_bolsa_familia')
