from polls.crawler.crawler import Crawler
import pandas as pd


class Cruzamento:
    url_bolsa = "https://www.portaltransparencia.gov.br/beneficios/bolsa-familia?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&colunasSelecionadas=linkDetalhamento%2Cuf%2Cmunicipio%2Ccpf%2Cnis%2Cbeneficiario%2CvalorTotalPeriodo"
    url_auxilio = "https://www.portaltransparencia.gov.br/beneficios/auxilio-emergencial?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&colunasSelecionadas=linkDetalhamento%2Ccpf%2Cnis%2Cbeneficiario%2Cobservacao%2CvalorTotalPeriodo%2Cuf%2Cmunicipio"

    crawler = Crawler()

    def buscar_auxilio_bolsa(self, cidade="SANTA+CRUZ+DA+BAIXA+VERDE", nome="", nis="", bolsa=True, periodoDe="2020-01", periodoAte="2020-12"):
        periodoDe = periodoDe.split("-")
        periodoAte = periodoAte.split("-")

        de = "&de=01%2F" + periodoDe[1] + "%2F" + periodoDe[0]
        ate = "&ate=28%2F" + periodoAte[1] + "%2F" + periodoAte[0]

        estado = "&uf=PE&nomeMunicipio=" + cidade
        if nis != "":
            nis = "&cpfNisBeneficiario=" + nis
        if nome != "":
            nome = "&nomeBeneficiario=" + nome.replace(" ", "+")

        if bolsa:
            urlFinal = self.url_bolsa + de + ate + estado + nis + nome
        else:
            urlFinal = self.url_auxilio + de + ate + estado + nis + nome
        html = self.crawler.cruzar_auxilios(urlFinal, cidade.replace("+", " "))

        table = pd.read_html(html)[0]
        table = table.drop(columns=['Detalhar'])
        return table

    def buscar_auxilio_total(self, cidade, periodoDe="2020-01", periodoAte="2020-01"):
        periodoDe = periodoDe.split("-")
        periodoAte = periodoAte.split("-")
        de = "&de=01%2F" + periodoDe[1] + "%2F" + periodoDe[0]
        ate = "&ate=28%2F" + periodoAte[1] + "%2F" + periodoAte[0]
        estado = "&uf=PE&nomeMunicipio=" + cidade.replace("_", "+")

        urlFinal = self.url_auxilio + de + ate + estado
        total = self.crawler.cruzar_auxilios_total(urlFinal, cidade.replace("_", " "))
        return total

    def buscar_prefeitura(self, nome="", cidade=""):
        html = self.crawler.cruzar_prefeitura(servidor=nome, cidade=cidade)
        table_PF = pd.read_html(html)[0]
        table_PF = table_PF.drop_duplicates(subset="Nome", keep='first')
        return table_PF

    def buscar_orgaos_medicina(self, nome="", cidade=""):
        table_data = self.crawler.cruzar_orgaos_medicina(nome=nome, cidade=cidade)
        colunas = ["Nome", "CRM", "Data de Inscrição", "Data de Inscrição UF"]
        table_medicos = pd.DataFrame(table_data, columns=colunas)
        return table_medicos

    def buscar_orgaos_aob(self, nome=""):
        table_data = self.crawler.cruzar_orgaos_oab(nome=nome)
        colunas = ["Nome", "Tipo", "Nº Inscrição", "UF"]
        table_advogados = pd.DataFrame(table_data, columns=colunas)
        return table_advogados

    def buscar_orgaos_confea(self, nome=""):
        html_data = self.crawler.cruzar_orgaos_confea(nome=nome)
        table_engenheiros = pd.read_html(html_data)[0]
        return table_engenheiros

    def buscar_orgaos_cfo(self, nome=""):
        table_data = self.crawler.cruzar_orgaos_cfo(nome=nome)
        colunas = ["Nome"]
        table_dentistas = pd.DataFrame(table_data, columns=colunas)
        return table_dentistas

    def buscar_bases(self, base, nome="", nis="", cidade="", periodoDe="2020-01", periodoAte="2020-12", orgaos=""):
        cidade = cidade.replace("_", "+")
        cidade = cidade.replace(" ", "+")
        if base == "auxilio":
            table = self.buscar_auxilio_bolsa(cidade=cidade, nome=nome, nis=nis, bolsa=False, periodoDe=periodoDe, periodoAte=periodoAte)
        elif base == "bolsa":
            table = self.buscar_auxilio_bolsa(cidade=cidade, nome=nome, nis=nis, periodoDe=periodoDe, periodoAte=periodoAte)
        elif base == "orgao":

            if orgaos == "medicina":
                table = self.buscar_orgaos_medicina(nome=nome, cidade=cidade)
            elif orgaos == "advocacia":
                table = self.buscar_orgaos_aob(nome=nome)
            elif orgaos == "engenharia":
                table = self.buscar_orgaos_confea(nome=nome)
            elif orgaos == "odontologia":
                table = self.buscar_orgaos_cfo(nome=nome)

        elif base == "prefeitura":
            table = self.buscar_prefeitura(nome=nome, cidade=cidade)
        return table

    def cruzar_ambas(self, tableA, tableB, chave, sufixos=['A', 'B']):
        ambos = pd.merge(tableA, tableB, how='inner', on=chave, suffixes=sufixos)  # contém em ambas as bases
        ambos = ambos.sort_values(chave)
        ambos = ambos.drop_duplicates(subset=chave, keep='first')
        return ambos.to_html()

    def cruzar_diferenca(self, tableA, tableB, chave, sufixos=['A', 'B']):
        # tableB = tableB.drop(columns=['UF', 'CPF'])
        diferenca = tableA.merge(tableB, how='outer', on=chave, suffixes=sufixos, indicator=True).loc[
            lambda x: x['_merge'] == 'left_only']
        # tableB = tableB.drop(columns=['Nome'])
        # diferenca = diferenca.drop(columns=tableB.columns)
        return diferenca.to_html()
