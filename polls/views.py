import pdfkit
import pandas as pd

from django.http import HttpResponse
from django.shortcuts import render

from .crawler.crawler import Crawler
from .dao.dao_backup import DaoBackup
from .models import Backup, Grafico
from .util.cruzamento import Cruzamento
from .util.graph import Graph

crawler = Crawler()


def index(request):
    return render(request, 'polls/index.html')


def contatos(request):
    return render(request, "polls/contatos.html")


def cruzamento(request):
    return render(request, 'polls/cruzamento.html', {"todo_periodo": "checked='checked'"})


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
    print(base2)

    dao = DaoBackup()
    backup = dao.buscar_backup(base_principal=base1, base_secundaria=base2, municipio=municipio, orgao=orgaos,
                        tipo_cruzamento=tipoCruzamento, periodo_de=de, periodo_ate=ate, nome=nome, nis=nis)

    print(backup)
    if backup is None:

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

        backup = Backup()
        backup.base_principal = base1
        backup.base_secundaria = base2
        backup.municipio = municipio
        backup.orgao = orgaos
        backup.tipo_cruzamento = tipoCruzamento
        backup.periodo_de = de
        backup.periodo_ate = ate
        backup.nome = nome
        backup.nis = nis
        backup.resultado = pd.read_html(data)[0].to_json()
        dao.salvar(backup)
    else:
        print(backup.resultado)
        data = pd.read_json(backup.resultado).to_html()

    data = data.replace("NaN", "Não há").replace("nan", "Não há")
    return render(request, 'polls/cruzamento.html',
                  {'data': data, "nome": nome, "nis": nis,
                   tipoCruzamento: "selected", municipio: "selected", orgaos: "selected", base1: "selected",
                   base2 + "2": "selected", tipo_periodo: "checked='checked'", "de": de, "ate": ate})


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


def gerar_csv(request):
    htmlstring = request.POST.get('htmlstring')
    htmlstring = '<!DOCTYPE html><html lang="pt-br"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" ' \
                 'content="IE=edge"><meta name="viewport" content="width=device-width, ' \
                 'initial-scale=1.0"> </head><body> ' + htmlstring + ' </body></html> '
    dt_csv = pd.read_html(htmlstring)[0]

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="export.csv"'},
    )

    dt_csv.to_csv(path_or_buf=response, encoding='utf-8-sig', sep=';')
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

        dao = DaoBackup()
        backup = dao.buscar_grafico(tipo=tipoGrafico, municipio=municipio, periodo_de=de, periodo_ate=ate)
        if backup is None:
            if tipoGrafico == "valor":
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
                for periodo in range(int(periodo_de), int(periodo_ate) + 1):
                    periodo = str(periodo)
                    periodo = periodo[0:4] + "-" + periodo[4::]

                    for cidade in ["Triunfo", "Calumbi", "Floresta", "Mirandiba", "Santa Cruz da Baixa Verde",
                                   "Serra Talhada", "Sao Jose do Belmonte"]:
                        print(f"Cidade: {cidade} - Mês: {periodo}")
                        total = c.buscar_auxilio_total(cidade=cidade.replace(" ", "_").upper(), periodoDe=periodo,
                                                       periodoAte=periodo)
                        tabela.append([cidade, total, periodo + "-01"])

                tabelas = pd.DataFrame(tabela, columns=["Município", "Total", "Data"])
                data = g.get_context_total(tabelas)
                print(tabelas)

            backup = Grafico()
            backup.tipo = tipoGrafico
            backup.municipio = municipio
            backup.periodo_de = de
            backup.periodo_ate = ate
            backup.resultado = tabelas.to_json()

            print(backup.resultado)
            dao.salvar(backup)

        else:
            print(backup.resultado)
            tabelas = pd.read_json(backup.resultado)
            if tipoGrafico == "valor":
                data = g.get_context_valor(tabelas)
            else:
                data = g.get_context_total(tabelas)

        return render(request, "polls/analise.html",
                      {'data': data, "municipio": municipio, tipoGrafico: "selected", "de": de, "ate": ate})
    else:
        return render(request, "polls/analise.html")
