import re

from polls.crawler.crawler import Crawler
from polls.models import BolsaFamilia, AuxilioEmergencial
import pandas as pd
import numpy as np


class Cruzamento:
    url_bolsa = "https://www.portaltransparencia.gov.br/beneficios/bolsa-familia?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&colunasSelecionadas=linkDetalhamento%2Cuf%2Cmunicipio%2Ccpf%2Cnis%2Cbeneficiario%2CvalorTotalPeriodo"
    url_auxilio = "https://www.portaltransparencia.gov.br/beneficios/auxilio-emergencial?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&colunasSelecionadas=linkDetalhamento%2Ccpf%2Cnis%2Cbeneficiario%2Cobservacao%2CvalorTotalPeriodo%2Cuf%2Cmunicipio"
    sufixos = ['_BF', '_AE']

    crawler = Crawler()

    def dados_auxilio_bolsa(self, cidade="SANTA CRUZ DA BAIXA VERDE", nome="", nis="", bolsa=True):
        de = "&de=01%2F01%2F2020"
        ate = "&ate=31%2F12%2F2020"
        estado = "&uf=PE&nomeMunicipio=" + cidade.replace(" ", "+")

        if nis != "":
            nis = "&cpfNisBeneficiario=" + nis

        if nome != "":
            nome = "&nomeBeneficiario=" + nome.replace(" ", "+")

        if bolsa:
            urlFinal = self.url_bolsa + de + ate + estado + nis + nome
        else:
            urlFinal = self.url_auxilio + de + ate + estado + nis + nome
        html = self.crawler.cruzar_auxilios(urlFinal)
        return html

    def auxilio_bolsa(self, nome="", nis=""):
        html = self.dados_auxilio_bolsa(nome=nome, nis=nis, bolsa=True)
        table_BF = pd.read_html(html)[0]

        html = self.dados_auxilio_bolsa(nome=nome, nis=nis, bolsa=False)
        table_AE = pd.read_html(html)[0]

        table_AE = table_AE.drop(columns=['Detalhar'])
        table_BF = table_BF.drop(columns=['Detalhar'])

        return {"ae": table_AE, "bf": table_BF}

    def cruzar_ae_bf_indevidos(self, nome="", nis="", base1="bf", base2="ae"):
        bases = self.auxilio_bolsa(nome=nome, nis=nis)
        table1 = bases[base1]
        table2 = bases[base2]

        indevido = pd.merge(table2, table1, how='inner', on='NIS', suffixes=self.sufixos)  # recebeu ambos (BF e AE)
        return indevido.to_html()

    def cruzar_nao_bolsa(self, nome="", nis="", base1="bf", base2="ae"):
        bases = self.auxilio_bolsa(nome=nome, nis=nis)
        table1 = bases[base1]
        table2 = bases[base2]

        devia_receber = table1.merge(table2, how='outer', on='NIS', suffixes=self.sufixos, indicator=True).loc[
            lambda x: x['_merge'] == 'left_only']
        return devia_receber.to_html()
