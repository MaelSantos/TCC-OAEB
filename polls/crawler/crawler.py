from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait


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
        # chrome_options.add_argument("--headless")  ## faz com que o browser não abra durante o processo
        driver = webdriver.Chrome(executable_path='chromedriver',
                                  options=chrome_options)  ## caminho para o seu webdriver

        driver.implicitly_wait(100000)
        driver.get(url)  ## carrega a página (htlm, js, etc.)

        # driver.find_element_by_id(id)
        # WebDriverWait(driver, 100)
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

        de = "&de=01%2F"+listDe[1]+"%2F"+listDe[0]
        ate = "&ate=31%2F"+listAte[1]+"%2F"+listAte[0]

        url = "https://www.portaltransparencia.gov.br/beneficios/bolsa-familia?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&colunasSelecionadas=linkDetalhamento%2Cuf%2Cmunicipio%2Ccpf%2Cnis%2Cbeneficiario%2CvalorTotalPeriodo&uf=PE&nomeMunicipio=TRIUNFO"

        linkTotal = url + nis + nome + de + ate
        print(linkTotal)

        html = self.buscar(linkTotal, "lista")

        soup = BeautifulSoup(html, 'html.parser')
        tabela = soup.find("table", id="lista")  ## busca tabela com dados
        return tabela.prettify()
