import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


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
        driver.get(url)  ## carrega a página (html, js, etc.)
        time.sleep(3)

        body = driver.find_element(By.ID, "lista").find_element(By.XPATH, "tbody").text
        if "Nenhum registro encontrado" in body:
            driver.refresh()  # evitar erros da pagina do auxilio
            time.sleep(4)

        driver.find_element(By.CLASS_NAME, "botao__gera_paginacao_completa").click() #exibe toda a paginação
        time.sleep(3)

        select = Select(driver.find_element(By.NAME, "lista_length"))
        select.select_by_value('50') #seleciona a quantidade maxima de exibição

        time.sleep(3)
        text_total = driver.find_element(By.ID, "lista_info").get_attribute('innerHTML')
        total = text_total.split(" ")[-1]

        html = "<table>"
        tbody = driver.find_element(By.ID, "lista").find_element(By.XPATH, "tbody").get_attribute('outerHTML')
        thead = driver.find_element(By.ID, "lista").find_element(By.XPATH, "thead").get_attribute('outerHTML')\
            .replace("NIS Beneficiário", "NIS")

        if int(total) > 0:
            for i in range(int(total)-1): # extrai as informações de todas as paginas
                driver.find_element(By.ID, "lista_next").click()
                time.sleep(5)
                tbody += driver.find_element(By.ID, "lista").find_element(By.XPATH, "tbody").get_attribute('outerHTML')

        html += thead + tbody + "</table>"

        return html
