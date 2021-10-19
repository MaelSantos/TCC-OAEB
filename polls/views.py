from builtins import type

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


def busca(request):
    return render(request, 'polls/busca_beneficiario.html')


def buscar(request):
    if request.method == "POST":
        nome = request.POST.get('nomeBeneficiario')
        nis = request.POST.get('nis')
        tipoBusca = request.POST.get('tipoBusca')
        cidade = request.POST.get('cidade')

        de = request.POST.get('de')
        ate = request.POST.get('ate')
        periodo = request.POST.get('periodo')

        if tipoBusca == "prefeitura":
            bolsa = ""
            prefeitura = "selected"
            periodo_prefeitura = periodo.split('-')
            mes = periodo_prefeitura[1]
            ano = periodo_prefeitura[0]
            html = crawler.crawler_prefeitura(cidade, nome, mes, ano)
        elif tipoBusca == "bolsa":
            prefeitura = ""
            bolsa = "selected"
            html = crawler.crawler_bolsafamilia(nome, nis, de, ate)

        return render(request, 'polls/busca_beneficiario.html', {'data': html, "nome": nome, "nis": nis,
                                                                 "prefeitura": prefeitura, "bolsa": bolsa,
                                                                 cidade: "selected", "de": de, "ate": ate,
                                                                 "periodo": periodo})
    else:
        return redirect('buscar')


def bolsa_famila(request):
    return render(request, "polls/bolsa_familia.html")


def buscar_bolsa_famila(request):
    if request.method == "POST":
        nome = request.POST.get('nomeBeneficiario')
        nis = request.POST.get('nis')
        tipoBusca = request.POST.get('tipoBusca')

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

        # print(data)

        return render(request, 'polls/bolsa_familia.html',
                      {'data': data, "nome": nome, "nis": nis, "devido": devido, "indevido": indevido})
    else:
        return redirect('busca_bolsa_familia')


def cruzamento(request):
    return render(request, 'polls/cruzamento.html')


def cruzar(request):
    return render(request, 'polls/cruzamento.html')
