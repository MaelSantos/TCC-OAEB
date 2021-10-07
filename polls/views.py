from django.shortcuts import render, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .crawler.crawler import Crawler
from .models import BeneficiarioAuxilio, BeneficiarioBolsaFamilia

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
        tipoBusca = request.POST.get('tipoBusca')
        # cpf = request.POST.get('cpf')

        if tipoBusca == "d":
            devido = "selected"
            indevido = ""

            data = session.query(BeneficiarioAuxilio).filter(
                BeneficiarioAuxilio.nome_beneficiario.like("%" + nome + "%")) \
                .filter(BeneficiarioBolsaFamilia.nome_favorecido.like("%" + nome + "%")) \
                .filter(BeneficiarioAuxilio.nis.like("%" + nis + "%")) \
                .filter(BeneficiarioBolsaFamilia.nis.like("%" + nis + "%")) \
                .filter(BeneficiarioBolsaFamilia.nis == BeneficiarioAuxilio.nis)
        else:
            devido = ""
            indevido = "selected"

            data = session.query(BeneficiarioBolsaFamilia).filter(
                BeneficiarioBolsaFamilia.nome_favorecido.like("%" + nome + "%")) \
                .filter(BeneficiarioBolsaFamilia.nis.like("%" + nis + "%")) \
                .filter(BeneficiarioBolsaFamilia.nis.not_in(session.query(BeneficiarioAuxilio.nis).filter(
                    BeneficiarioAuxilio.nome_beneficiario.like("%" + nome + "%")).filter(
                    BeneficiarioAuxilio.nis.like("%" + nis + "%")))).group_by(BeneficiarioBolsaFamilia.nis)

        print(data)

        return render(request, 'polls/bolsa_familia.html',
                      {'data': data, "nome": nome, "nis": nis, "devido": devido, "indevido": indevido})
    else:
        return redirect('cruzar_bolsa_familia')
