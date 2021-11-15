import base64

from django.http import HttpResponse
from django.shortcuts import render, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pdfkit

from .crawler.crawler import Crawler
from .models import BeneficiarioAuxilio, BeneficiarioBolsaFamilia
from .controller.cruzamento import Cruzamento

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
    nome = request.POST.get('nomeBeneficiario')
    nis = request.POST.get('nis')
    tipoCruzamento = request.POST.get('tipoCruzamento')
    municipio = request.POST.get('municipio')
    orgaos = request.POST.get('orgaos')

    tipo_periodo = request.POST.get('tipo_periodo')
    de = request.POST.get('de')
    ate = request.POST.get('ate')
    if de == "" or ate == "":
        de = "2020-01"
        ate = "2020-12"
    base1 = request.POST.get('base1')
    base2 = request.POST.get('base2')

    c = Cruzamento()
    tableA = c.buscar_bases(base1, nome=nome, nis=nis, cidade=municipio, periodoDe=de, periodoAte=ate, orgaos=orgaos)

    if base2 != "":
        sufixos = ["_" + base1[0:2].upper(), "_" + base2[0:2].upper()]
        if base1 == "auxilio" and base2 == "bolsa":
            chave = "NIS"
        else:
            chave = "Nome"

        tableB = c.buscar_bases(base2, nome=nome, nis=nis, cidade=municipio, periodoDe=de, periodoAte=ate, orgaos=orgaos)
        if tipoCruzamento == "intersecao":
            data = c.cruzar_ambas(tableA, tableB, chave, sufixos)
        else:
            data = c.cruzar_diferenca(tableA, tableB, chave, sufixos)
    else:
        data = tableA.to_html()

    print(tipo_periodo)

    return render(request, 'polls/cruzamento.html',
                  {'data': data, "nome": nome, "nis": nis, tipoCruzamento: "selected", municipio: "selected",
                   orgaos: "selected", base1: "selected", base2 + "2": "selected", tipo_periodo: "checked", "de": de,
                   "ate": ate})


def gerar_pdf(request):
    htmlstring = request.POST.get('htmlstring')

    htmlstring = '<!DOCTYPE html><html lang="pt-br"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" ' \
                 'content="IE=edge"><meta name="viewport" content="width=device-width, ' \
                 'initial-scale=1.0"> </head><body> ' + htmlstring + ' </body></html> '

    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(htmlstring, False, options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="export.pdf"'
    return response


def denuncie(request):
    return render(request, "polls/denuncie.html")
