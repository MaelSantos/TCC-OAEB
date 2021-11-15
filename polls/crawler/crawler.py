import time
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class Crawler:
    url_padrao = "folha-pagamentos/servidoresAtivos?"

    urls = {
        "TRIUNFO": "https://triunfo.pe.gov.br/transparencia/folha-pagamentos/servidoresAtivos/",
        "CALUMBI": "https://calumbi.pe.gov.br/transparencia/folha-pagamentos/servidoresAtivos/",
        "FLORESTA": "https://floresta.pe.gov.br/transparencia/folha-pagamentos/servidoresAtivos/",
        "MIRANDIBA": "https://mirandiba.pe.gov.br/portal-transparencia/folha-pagamentos/servidoresAtivos/",
        "SANTA+CRUZ+DA+BAIXA+VERDE": "https://santacruzdabaixaverde.pe.gov.br/transparencia/folha-pagamentos/servidoresAtivos/",
        # "BETANIA": "https://betania.pe.gov.br/folha-de-pagamento/",
        "SERRA+TALHADA": "http://transparencia.serratalhada.pe.gov.br/FolhasPagamentosServidores/ativos/",
        "SAO+JOSE+DO+BELMONTE": "https://saojosedobelmonte.pe.gov.br/portal-transparencia/folha-pagamentos/servidoresAtivos/"
    }

    codigos = {
        "TRIUNFO": "5483",
        "CALUMBI": "5197",
        "FLORESTA": "5255",
        "MIRANDIBA": "5345",
        "SANTA+CRUZ+DA+BAIXA+VERDE": "5421",
        "SERRA+TALHADA": "5453",
        "SAO+JOSE+DO+BELMONTE": "5442"
    }

    def criar_crawler(self, ocultar_pagina=False):
        chrome_options = Options()
        if ocultar_pagina:
            chrome_options.add_argument("--headless")  ## faz com que o browser não abra durante o processo
        driver = webdriver.Chrome(executable_path='chromedriver',
                                  options=chrome_options)  ## caminho para o seu webdriver
        driver.implicitly_wait(3)
        return driver

    def selecionar_select(self, driver, nome, valor, tipo="id"):
        select = Select(driver.find_element(tipo, nome))
        select.select_by_value(valor)  # seleciona a uf PE

    def buscar(self, url, id=""):
        driver = self.criar_crawler()
        driver.get(url)  ## carrega a página (htlm, js, etc.)
        time.sleep(1)
        # tabela = driver.find_element_by_id(id)

        # WebDriverWait(driver, 1000000).until(lambda d: d.find_element_by_id(id))
        html = driver.page_source

        return html

    def crawler_prefeitura(self, cidade, servidor, mes='4', ano='2020'):

        url = self.urls[cidade] + "?ano=" + ano + "&servidor=" + servidor.upper() + "&mes=" + mes
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
        driver = self.criar_crawler()

        print(url)
        driver.get(url)  ## carrega a página (html, js, etc.)
        time.sleep(3)

        body = driver.find_element(By.ID, "lista").find_element(By.XPATH, "tbody").text
        if "Nenhum registro encontrado" in body:
            driver.refresh()  # evitar erros da pagina do auxilio
            time.sleep(4)

        driver.find_element(By.CLASS_NAME, "botao__gera_paginacao_completa").click()  # exibe toda a paginação
        time.sleep(3)

        self.selecionar_select(driver, "lista_length", "50", By.NAME)  # seleciona a quantidade maxima de exibição
        # select = Select(driver.find_element(By.NAME, "lista_length"))
        # select.select_by_value('50')

        time.sleep(3)
        text_total = driver.find_element(By.ID, "lista_info").get_attribute('innerHTML')
        total = text_total.split(" ")[-1]

        html = "<table>"
        tbody = driver.find_element(By.ID, "lista").find_element(By.XPATH, "tbody").get_attribute('outerHTML')
        thead = driver.find_element(By.ID, "lista").find_element(By.XPATH, "thead").get_attribute('outerHTML') \
            .replace("NIS Beneficiário", "NIS").replace("CPF Beneficiário", "CPF").replace("Beneficiário",
                                                                                           "Nome").replace(
            "BENEFICIÁRIO", "Nome")

        if int(total) > 0:
            for i in range(int(total) - 1):  # extrai as informações de todas as paginas
                driver.find_element(By.ID, "lista_next").click()
                time.sleep(5)
                tbody += driver.find_element(By.ID, "lista").find_element(By.XPATH, "tbody").get_attribute('outerHTML')
                print(i)

        html += thead + tbody + "</table>"

        return html

    def cruzar_prefeitura(self, cidade="SANTA+CRUZ+DA+BAIXA+VERDE", servidor="", mes='', ano='2020'):

        url = self.urls[cidade] + "?ano=" + ano + "&servidor=" + servidor + "&mes=" + mes
        print(url)

        driver = self.criar_crawler()

        driver.get(url)
        time.sleep(3)
        html = "<table>"
        tbody = driver.find_element(By.ID, "table").find_element(By.XPATH, "tbody").get_attribute('outerHTML')
        thead = driver.find_element(By.ID, "table").find_element(By.XPATH, "thead").get_attribute('outerHTML')

        text_total = driver.find_element(By.CLASS_NAME, "paginator").find_element(By.TAG_NAME, "p").get_attribute(
            'innerHTML')
        total = text_total.split(" ")[-1]

        if int(total) > 0:
            for i in range(int(total) - 1):  # extrai as informações de todas as paginas
                time.sleep(10)
                driver.find_element(By.CLASS_NAME, "next").find_element(By.TAG_NAME, "a").click()
                time.sleep(5)
                tbody += driver.find_element(By.ID, "table").find_element(By.XPATH, "tbody").get_attribute('outerHTML')

        html += thead + tbody + "</table>"

        return html

    def cruzar_orgaos_medicina(self, nome="", cidade="SANTA+CRUZ+DA+BAIXA+VERDE"):
        url = "https://portal.cfm.org.br/busca-medicos/"
        driver = self.criar_crawler()
        driver.get(url)

        if nome != "":
            elemento_nome = driver.find_element(By.NAME, "nome")
            elemento_nome.clear()
            elemento_nome.send_keys(nome)
        self.selecionar_select(driver, "uf", "PE", By.ID)  # seleciona UF
        self.selecionar_select(driver, "municipio", self.codigos[cidade], By.ID)  # seleciona municipio
        driver.find_element(By.CLASS_NAME, "button").click()  # aceita cookies
        driver.find_element(By.CLASS_NAME, "btnPesquisar").click()  # busca informações
        time.sleep(5)

        try:
            total = driver.find_elements(By.CLASS_NAME, "J-paginationjs-page")[-1].text
        except Exception:
            total = 1

        medicos = []
        for i in range(int(total)):
            try:
                for j in range(10):
                    campo_medico = driver.find_element(By.CLASS_NAME, f"resultMedico_{j}").find_element(By.CLASS_NAME,
                                                                                                        "card-body")
                    nome = campo_medico.find_element(By.TAG_NAME, "h4").text.upper()
                    campos = campo_medico.find_element(By.CLASS_NAME, "row").find_elements(By.CLASS_NAME, "col-md-4")
                    crm = campos[0].text.split(" ")[-1]
                    data_inscricao = campos[1].text.split(" ")[-1]
                    data_uf = campos[2].text.split(" ")[-1]
                    medicos.append([nome, crm, data_inscricao, data_uf])
            except Exception:
                break
            if total != 1:
                driver.find_element(By.XPATH, f"//li[@data-num='{(i + 1)}']").click()
                time.sleep(3)

        return medicos

    def cruzar_orgaos_oab(self, nome):
        url = "https://cna.oab.org.br/"
        driver = self.criar_crawler()
        driver.get(url)

        elemento_nome = driver.find_element(By.NAME, "NomeAdvo")
        elemento_nome.clear()
        elemento_nome.send_keys(nome)
        self.selecionar_select(driver, "cmbSeccional", "PE", By.ID)  # seleciona UF

        site_key = driver.find_element(By.CLASS_NAME, "g-recaptcha").get_attribute("data-sitekey")
        captcha_token = self.resolver_catcha(url, site_key)
        driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML = "{captcha_token}"')
        time.sleep(3)
        driver.find_element(By.ID, "btnFind").click()  # busca informações
        time.sleep(3)

        resultados = driver.find_element(By.ID, "divResult").find_elements(By.CLASS_NAME, "row")

        advogados = []
        for r in resultados:
            nome = r.find_element(By.CLASS_NAME, "rowName").find_elements(By.XPATH, "span")[-1].text
            tipo = r.find_element(By.CLASS_NAME, "rowTipoInsc").find_elements(By.XPATH, "span")[-1].text
            inscricao = r.find_element(By.CLASS_NAME, "rowInsc").find_elements(By.XPATH, "span")[-1].text
            uf = r.find_element(By.CLASS_NAME, "rowUf").find_elements(By.XPATH, "span")[-1].text
            advogados.append([nome, tipo, inscricao, uf])
        return advogados

    def cruzar_orgaos_confea(self, nome):
        url = "https://consultaprofissional.confea.org.br/"
        driver = self.criar_crawler()
        driver.get(url)

        elemento_nome = driver.find_element(By.ID, "ContentPlaceHolder1_txtNome")
        elemento_nome.clear()
        elemento_nome.send_keys(nome)

        site_key = driver.find_element(By.CLASS_NAME, "g-recaptcha").get_attribute("data-sitekey")
        captcha_token = self.resolver_catcha(url, site_key)
        driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML = "{captcha_token}"')
        driver.find_element(By.ID, "ContentPlaceHolder1_btnBuscar").click()  # busca informações
        time.sleep(3)

        html = "<table>"
        elementos_table = driver.find_element(By.ID, "ContentPlaceHolder1_gvResultado")
        thead = elementos_table.find_element(By.TAG_NAME, "tbody").find_element(By.TAG_NAME, "tr").get_attribute(
            'outerHTML')
        thead = "</thead>" + thead + "</thead>"
        driver.execute_script('document.getElementsByTagName("tr")[0].remove()')
        tbody = elementos_table.find_element(By.TAG_NAME, "tbody").get_attribute('outerHTML')

        fim = False

        contador = 2
        try:
            while not fim:
                driver.find_element(By.XPATH, f"//*[contains(text(), '{contador}')]").click()
                time.sleep(5)
                elementos_table = driver.find_element(By.ID, "ContentPlaceHolder1_gvResultado")
                driver.execute_script('document.getElementsByTagName("tr")[0].remove()')
                tbody += elementos_table.find_element(By.XPATH, "tbody").get_attribute('outerHTML')
                contador += 1
        except:
            pass
        html += thead + tbody + "</table>"
        return html

    def cruzar_orgaos_cfo(self, nome):
        url = "https://website.cfo.org.br/profissionais-cadastrados/"
        driver = self.criar_crawler()
        driver.get(url)

        elemento_nome = driver.find_element(By.NAME, "nome")
        elemento_nome.clear()
        elemento_nome.send_keys(nome)
        self.selecionar_select(driver, "cro", "PE", By.NAME)

        driver.find_element(By.ID, "btnConsulta").click()
        time.sleep(3)

        dentistas = []
        proximo = driver.find_element(By.XPATH, "//*[contains(text(), 'Próxima')]")
        try:
            nomes = driver.find_elements(By.TAG_NAME, "b")
            for n in nomes:
                dentistas.append(n.text)
            while proximo.text == "Próxima":
                proximo.click()
                time.sleep(3)
                nomes = driver.find_elements(By.TAG_NAME, "b")
                for n in nomes:
                    dentistas.append(n.text)
                proximo = driver.find_element(By.XPATH, "//*[contains(text(), 'Próxima')]")
        except Exception:
            print("Fim")
        return dentistas

    def resolver_catcha(self, site_url, site_key):
        chave_api = "35f5532bbd7faa4e32db0a180b52e766"
        link_solicitacao = f"http://2captcha.com/in.php?key={chave_api}&method=userrecaptcha&googlekey={site_key}&pageurl={site_url}&json=true"

        resposta_solicitacao = requests.get(link_solicitacao).json()
        print(resposta_solicitacao)
        captcha_id = resposta_solicitacao.get("request")
        captcha_token = "CAPCHA_NOT_READY"

        link_requisicao = f"http://2captcha.com/res.php?key={chave_api}&action=get&id={captcha_id}&json=true"
        while captcha_token == "CAPCHA_NOT_READY":
            time.sleep(10)
            resposta_requisicao = requests.get(link_requisicao).json()
            print(resposta_requisicao)
            if resposta_requisicao.get("status") == 1:
                captcha_token = resposta_requisicao.get("request")

        return captcha_token


c = Crawler()
d = c.cruzar_orgaos_confea("JOÃO")
print(d)
