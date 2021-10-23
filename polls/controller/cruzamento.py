import re

from polls.crawler.crawler import Crawler
from polls.models import BolsaFamilia, AuxilioEmergencial
import pandas as pd
import numpy as np


class Cruzamento:
    url_bolsa = "https://www.portaltransparencia.gov.br/beneficios/bolsa-familia?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&colunasSelecionadas=linkDetalhamento%2Cuf%2Cmunicipio%2Ccpf%2Cnis%2Cbeneficiario%2CvalorTotalPeriodo"
    url_auxilio = "https://www.portaltransparencia.gov.br/beneficios/auxilio-emergencial?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&colunasSelecionadas=linkDetalhamento%2Ccpf%2Cnis%2Cbeneficiario%2Cobservacao%2CvalorTotalPeriodo%2Cuf%2Cmunicipio"

    crawler = Crawler()

    def dados_bolsa(self, cidade="SANTA CRUZ DA BAIXA VERDE", nome="", nis=""):
        # BF
        de = "&de=01%2F01%2F2020"
        ate = "&ate=31%2F12%2F2020"
        estado = "&uf=PE&nomeMunicipio=" + cidade.replace(" ", "+")

        urlFinal = self.url_bolsa + de + ate + estado
        html = self.crawler.cruzar_auxilios(urlFinal)
        return html

        beneficiarios = html.split("\n")

        for b in beneficiarios:
            text_formatado = b.replace("-", ",").replace("*", "0").replace(".", "")
            list_beneficiario = re.split(r'\s(?=\d+)', text_formatado)
            print(list_beneficiario)

            bf = BolsaFamilia()
            bf.uf = list_beneficiario[0][9:11]
            bf.municipio = cidade
            cpf = list_beneficiario[1].replace(",", "")
            bf.cpf = "***." + cpf[3:6] + "." + cpf[6:9] + "-**"
            bf.nis = list_beneficiario[2][0:12].replace(",", "").replace(".", "")
            bf.nome = list_beneficiario[2][13::]
            bf.valor = list_beneficiario[3]

            # dao.create(c)
            print(bf)

    def dados_auxilio(self, cidade="SANTA CRUZ DA BAIXA VERDE", nome="", nis=""):
        # AE

        de = "&de=01%2F01%2F2020"
        ate = "&ate=31%2F12%2F2020"
        estado = "&uf=PE&nomeMunicipio=" + cidade.replace(" ", "+")
        urlFinal = self.url_auxilio + de + ate + estado
        html = self.crawler.cruzar_auxilios(urlFinal)
        return html

        beneficiarios = html.split("\n")

        for b in beneficiarios:
            text_formatado = b.replace("-", ",").replace("*", "0").replace(".", "")
            list_beneficiario = re.split(r'\s(?=\d+)', text_formatado)
            print(list_beneficiario)

            quantidade = len(list_beneficiario)

            a = AuxilioEmergencial()
            a.uf = list_beneficiario[0][9:11]
            a.municipio = cidade

            if quantidade == 4:
                a.nis = list_beneficiario[2][0:12].replace(",", "")
                nome_obs = list_beneficiario[2][13::]
                cpf = list_beneficiario[1].replace(",", "")
            else:
                a.nis = ""
                cpf = list_beneficiario[1][0:12].replace(",", "")
                nome_obs = list_beneficiario[1][13::]

            a.cpf = "***." + cpf[3:6] + "." + cpf[6:9] + "-**"
            index_obs = nome_obs.find("Não há")

            if index_obs == -1:
                index_obs = nome_obs.find("Valor devolvido à União.")
            if index_obs == -1:
                index_obs = nome_obs.find("Pagamento bloqueado ou cancelado")
            if index_obs != -1:
                a.observacao = nome_obs[index_obs::]
                a.nome = nome_obs[0:index_obs - 1]
            else:
                a.observacao = "Não há"
                a.nome = nome_obs

            print(index_obs)
            if quantidade == 4:
                a.valor = list_beneficiario[3]
            else:
                a.valor = list_beneficiario[2]

            # dao.create(a)

            print(str(quantidade) + ": " + a.nis + " - " + a.nome + " - " + a.cpf + " - " + a.observacao)


c = Cruzamento()

html = c.dados_bolsa()
table_BF = pd.read_html(html)[0]
print(len(table_BF))
print(table_BF)

html = c.dados_auxilio()
table_AE = pd.read_html(html)[0]
print(len(table_AE))
print(table_AE)

sufixos = ['_BF', '_AE']

indevido = pd.merge(table_BF, table_AE, how='inner', on='NIS', suffixes=sufixos)  # recebeu ambos (BF e AE)
print(indevido)

# recebeu somente BF
# devia_receber = table_BF.compare(table_AE)
# devia_receber = pd.concat([table_BF, table_AE], keys='NIS').drop_duplicates(keep=False)
devia_receber = table_BF.merge(table_AE, how='outer', on='NIS', suffixes=sufixos, indicator=True).loc[lambda x: x['_merge'] == 'left_only']
print(devia_receber)
