import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

from polls.dao.dao import Dao
from polls.models import Cruzamento

class Crawler:
    url_padrao = "folha-pagamentos/servidoresAtivos?"

    urls = {
        "Triunfo": "https://triunfo.pe.gov.br/transparencia/",
        "Calumbi": "https://calumbi.pe.gov.br/transparencia/",
        "Floresta": "https://floresta.pe.gov.br/transparencia/",
        "Mirandiba": "https://mirandiba.pe.gov.br/portal-transparencia/",
        "SantaCruz": "https://www.santacruzdabaixaverde.pe.gov.br/transparencia/",
        "Betania": "https://betania.pe.gov.br/folha-de-pagamento/",
        "Serra": "http://transparencia.serratalhada.pe.gov.br/folhas-pagamentos-servidores/ativos?"
    }

    def buscar(self, url, id=""):
        chrome_options = Options()
        if id == "table":
            chrome_options.add_argument("--headless")  ## faz com que o browser não abra durante o processo
        driver = webdriver.Chrome(executable_path='chromedriver',
                                  options=chrome_options)  ## caminho para o seu webdriver

        driver.implicitly_wait(3)
        driver.get(url)  ## carrega a página (htlm, js, etc.)
        time.sleep(1)
        # tabela = driver.find_element_by_id(id)

        # WebDriverWait(driver, 1000000).until(lambda d: d.find_element_by_id(id))
        html = driver.page_source

        return html

    def crawler_prefeitura(self, cidade, servidor, mes='4', ano='2021'):

        if cidade != "Serra":
            url = self.urls[
                      cidade] + "folha-pagamentos/servidoresAtivos?ano=" + ano + "&servidor=" + servidor + "&mes=" + mes
        else:
            url = self.urls[cidade] + "?ano=" + ano + "&servidor=" + servidor + "&mes=" + mes
        print(url)

        html = self.buscar(url, "table")

        soup = BeautifulSoup(html, 'html.parser')
        tabela = soup.find("table", id="table")  ## busca tabela com dados
        return tabela.prettify()

    def crawler_bolsafamilia(self, nome="", nis="", de='2020-01', ate='2021-12'):

        if nis != "":
            nis = "&cpfNisBeneficiario=" + nis  # &cpfNisBeneficiario=2.362.676.777-5

        if nome != "":
            nome = "&nomeBeneficiario=" + nome.replace(" ", "+")  # &nomeBeneficiario=ACUCENA+DIAS+DO+NASCIMENTO+SANTOS

        listDe = de.split("-")
        listAte = ate.split("-")

        de = "&de=01%2F" + listDe[1] + "%2F" + listDe[0]
        ate = "&ate=31%2F" + listAte[1] + "%2F" + listAte[0]

        municipio = "&nomeMunicipio=SANTA+CRUZ+DA+BAIXA+VERDE"

        urlGeral = "https://www.portaltransparencia.gov.br/beneficios/bolsa-familia?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&colunasSelecionadas=linkDetalhamento%2Cuf%2Cmunicipio%2Ccpf%2Cnis%2Cbeneficiario%2CvalorTotalPeriodo&uf=PE"

        url = urlGeral + nis + nome + de + ate + municipio
        print(url)

        html = self.buscar(url, "lista")

        soup = BeautifulSoup(html, 'html.parser')
        tabela = soup.find("table", id="lista")  ## busca tabela com dados
        return tabela.prettify()

    def cruzar_auxilios(self, url):
        chrome_options = Options()
        # if id == "table":
        #     chrome_options.add_argument("--headless")  ## faz com que o browser não abra durante o processo
        driver = webdriver.Chrome(executable_path='chromedriver',
                                  options=chrome_options)  ## caminho para o seu webdriver
        print(url)
        driver.implicitly_wait(3)
        driver.get(url)  ## carrega a página (htlm, js, etc.)
        time.sleep(3)

        driver.find_element_by_class_name("botao__gera_paginacao_completa").click()
        time.sleep(3)

        select = Select(driver.find_element_by_name("lista_length"))
        select.select_by_value('50')

        time.sleep(3)
        text_total = driver.find_element_by_id("lista_info").get_attribute('innerHTML')
        total = text_total.split(" ")[-1]

        tbody = driver.find_element_by_id("lista").find_element_by_xpath("tbody").text  # get_attribute('innerHTML')
        for i in range(int(total)-1):
            print("pagina: " + str(i + 1))
            driver.find_element_by_id("lista_next").click()
            time.sleep(5)
            tbody += driver.find_element_by_id("lista").find_element_by_xpath("tbody").text+"\n" #get_attribute('innerHTML')

        return tbody


de = "&de=01%2F01%2F2020"
ate = "&ate=31%2F12%2F2020"
url = "https://www.portaltransparencia.gov.br/beneficios/bolsa-familia?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&colunasSelecionadas=linkDetalhamento%2Cuf%2Cmunicipio%2Ccpf%2Cnis%2Cbeneficiario%2CvalorTotalPeriodo&uf=PE&nomeMunicipio=SANTA+CRUZ+DA+BAIXA+VERDE";

c = Crawler()

html = c.cruzar_auxilios(url + de + ate)

# print(html)

beneficiarios = html.split("\n")

dao = Dao()
for b in beneficiarios:
    text_formatado = b.replace("-", ",").replace("*", "0")
    list_beneficiario = re.split(r'\s(?=\d+)', text_formatado)

    c = Cruzamento()

    c.estado = list_beneficiario[0][9:11]
    c.cidade = "SANTA CRUZ DA BAIXA VERDE"
    cpf = list_beneficiario[1].replace(",", "").replace(".", "")
    c.cpf = "***." + cpf[3:6] + "." + cpf[6:9] + "-**"
    c.nis = list_beneficiario[2][0:15].replace(",", "-")
    c.nome = list_beneficiario[2][16::]
    c.valor = list_beneficiario[3]
    c.tipo = "BF"

    # print(list_beneficiario)
    dao.create(c)
    print(c)


