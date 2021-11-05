import re

from polls.crawler.crawler import Crawler
from polls.models import BolsaFamilia, AuxilioEmergencial
import pandas as pd
import numpy as np


class Cruzamento:
    url_bolsa = "https://www.portaltransparencia.gov.br/beneficios/bolsa-familia?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&colunasSelecionadas=linkDetalhamento%2Cuf%2Cmunicipio%2Ccpf%2Cnis%2Cbeneficiario%2CvalorTotalPeriodo"
    url_auxilio = "https://www.portaltransparencia.gov.br/beneficios/auxilio-emergencial?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&colunasSelecionadas=linkDetalhamento%2Ccpf%2Cnis%2Cbeneficiario%2Cobservacao%2CvalorTotalPeriodo%2Cuf%2Cmunicipio"

    crawler = Crawler()

    def buscar_auxilio_bolsa(self, cidade="SANTA+CRUZ+DA+BAIXA+VERDE", nome="", nis="", bolsa=True):
        de = "&de=01%2F01%2F2020"
        ate = "&ate=31%2F12%2F2020"
        estado = "&uf=PE&nomeMunicipio=" + cidade
        if nis != "":
            nis = "&cpfNisBeneficiario=" + nis
        if nome != "":
            nome = "&nomeBeneficiario=" + nome.replace(" ", "+")

        if bolsa:
            urlFinal = self.url_bolsa + de + ate + estado + nis + nome
        else:
            urlFinal = self.url_auxilio + de + ate + estado + nis + nome
        html = self.crawler.cruzar_auxilios(urlFinal)

        table = pd.read_html(html)[0]
        table = table.drop(columns=['Detalhar'])
        return table

    def buscar_prefeitura(self, nome="", cidade=""):
        html = self.crawler.cruzar_prefeitura(servidor=nome, cidade=cidade)
        table_PF = pd.read_html(html)[0]
        return table_PF

    def buscar_orgaos(self, nome="", nis="", cidade=""):
        table_data = self.crawler.cruzar_orgaos_classe(nome=nome, cidade=cidade)
        colunas = ["Nome", "CRM", "Data de Inscrição", "Data de Inscrição UF"]
        table_medicos = pd.DataFrame(table_data, columns=colunas)
        return table_medicos

    def buscar_bases(self, base, nome="", nis="", cidade=""):
        cidade = cidade.replace("_", "+")
        if base == "auxilio":
            table = self.buscar_auxilio_bolsa(cidade=cidade, nome=nome, nis=nis, bolsa=False)
        elif base == "bolsa":
            table = self.buscar_auxilio_bolsa(cidade=cidade, nome=nome, nis=nis)
        elif base == "orgao":
            table = self.buscar_orgaos(nome=nome, cidade=cidade)
        elif base == "prefeitura":
            table = self.buscar_prefeitura(nome=nome, cidade=cidade)
        return table

    def cruzar_ambas(self, tableA, tableB, chave, sufixos=['A', 'B']):
        ambos = pd.merge(tableA, tableB, how='inner', on=chave, suffixes=sufixos)  # contém em ambas as bases
        ambos = ambos.sort_values(chave)
        ambos = ambos.drop_duplicates(subset=chave, keep='first')
        return ambos.to_html()

    def cruzar_diferenca(self, tableA, tableB, chave, sufixos=['A', 'B']):
        diferenca = tableA.merge(tableB, how='outer', on=chave, suffixes=sufixos, indicator=True).loc[lambda x: x['_merge'] == 'left_only']
        tableB = tableB.drop(columns=["Nome"])
        diferenca = diferenca.drop(columns=tableB.columns)
        return diferenca.to_html()
