import pdfkit
import pandas as pd

from django.http import HttpResponse
from django.shortcuts import render, redirect

from .crawler.crawler import Crawler
from .util.cruzamento import Cruzamento
from .util.graph import Graph

crawler = Crawler()


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

        tableB = c.buscar_bases(base2, nome=nome, nis=nis, cidade=municipio, periodoDe=de, periodoAte=ate,
                                orgaos=orgaos)
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


def analise(request):
    if request.method == "POST":
        municipio = request.POST.get('municipio')
        tipoGrafico = request.POST.get('tipoGrafico')
        de = request.POST.get('de')
        ate = request.POST.get('ate')
        c = Cruzamento()
        g = Graph()

        if de == "":
            periodo_de = "202004"
        else:
            periodo_de = de.replace("-", "")
        if ate == "":
            periodo_ate = "202012"
        else:
            periodo_ate = ate.replace("-", "")

        tabelas = None
        if tipoGrafico == "":
            for periodo in range(int(periodo_de), int(periodo_ate) + 1):
                periodo = str(periodo)
                periodo = periodo[0:4] + "-" + periodo[4::]

                tabela = c.buscar_bases("auxilio", nome="", cidade=municipio, periodoDe=periodo, periodoAte=periodo)
                tabela.insert(0, "Data", periodo)

                if tabelas is not None:
                    tabelas = pd.concat([tabelas, tabela])
                else:
                    tabelas = tabela

            tabelas['Valor Disponibilizado (R$)'] = tabelas['Valor Disponibilizado (R$)'].apply(g.format_valor)
            tabelas = tabelas.groupby(['Valor Disponibilizado (R$)', 'Data'], as_index=False)['UF'].count()
            tabelas = tabelas.rename(columns={'UF': 'Quantidade'})

            print(tabelas)
            data = g.get_context_valor(tabelas)
        else:
            tabela = []
            for cidade in ["Triunfo", "Calumbi", "Floresta", "Mirandiba", "Santa Cruz da Baixa Verde",
                           "Serra Talhada", "Sao Jose do Belmonte"]:
                for periodo in range(int(periodo_de), int(periodo_ate) + 1):
                    periodo = str(periodo)
                    periodo = periodo[0:4] + "-" + periodo[4::]

                    total = c.buscar_auxilio_total(cidade=cidade.replace(" ", "+").upper(), periodoDe=periodo, periodoAte=periodo)
                    tabela.append([cidade, total, periodo])

            tabelas = pd.DataFrame(tabela, columns=["Município", "Total", "Data"])
            print(tabelas)
            data = g.get_context_total(tabelas)

        return render(request, "polls/analise.html", {'data': data, municipio: "selected", tipoGrafico: "selected", "de": de, "ate": ate})
    else:
        return render(request, "polls/analise.html")
