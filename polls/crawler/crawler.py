from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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

    def buscar(self, url):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  ## faz com que o browser não abra durante o processo
        driver = webdriver.Chrome(executable_path='chromedriver',
                                  options=chrome_options)  ## caminho para o seu webdriver

        driver.implicitly_wait(10)
        driver.get(url)  ## carrega a página (htlm, js, etc.)

        driver.find_element_by_id("lista")
        html = driver.page_source

        return html

    def crawler_prefeitura(self, cidade, servidor, mes='4', ano='2021'):

        if cidade != "Serra":
            url = self.urls[
                      cidade] + "folha-pagamentos/servidoresAtivos?ano=" + ano + "&servidor=" + servidor + "&mes=" + mes
        else:
            url = self.urls[cidade] + "?ano=" + ano + "&servidor=" + servidor + "&mes=" + mes
        print(url)

        html = self.buscar(url)

        soup = BeautifulSoup(html, 'html.parser')
        tabela = soup.find("table", id="table")  ## busca tabela com dados
        return tabela

    def crawler_bolsafamilia(self):

        # nis = "&cpfNisBeneficiario=2.362.676.777-5"
        # url = "https://www.portaltransparencia.gov.br/beneficios/bolsa-familia?uf=PE&municipio=18443&de=01/01/2020&ate=31/12/2020&tipoBeneficio=1&nomeMunicipio=TRIUNFO&ordenarPor=beneficiario&direcao=asc"+nis
        # print(url)

        html = self.buscar("https://www.portaltransparencia.gov.br/beneficios/bolsa-familia?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&colunasSelecionadas=linkDetalhamento%2Cuf%2Cmunicipio%2Ccpf%2Cnis%2Cbeneficiario%2CvalorTotalPeriodo&de=01%2F01%2F2020&ate=31%2F12%2F2020&uf=PE&nomeMunicipio=TRIUNFO&cpfNisBeneficiario=2.362.676.777-5")

        soup = BeautifulSoup(html, 'html.parser')
        tabela = soup.find("table", id="lista")  ## busca tabela com dados
        return tabela
