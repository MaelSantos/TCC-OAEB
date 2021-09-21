from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests

urlTriunfo = "https://triunfo.pe.gov.br/transparencia/"
urlCalumbi = "https://calumbi.pe.gov.br/transparencia/"
urlFloresta = "https://floresta.pe.gov.br/transparencia/"
urlMirandiba = "https://mirandiba.pe.gov.br/portal-transparencia/"
urlSantaCruz = "https://www.santacruzdabaixaverde.pe.gov.br/transparencia/"
urlBetania = "https://betania.pe.gov.br/folha-de-pagamento/";

urlSerra = "http://transparencia.serratalhada.pe.gov.br/folhas-pagamentos-servidores/ativos?ano=2021"

servidor = "&servidor=joao"
mes = "&mes=3"

url = urlSantaCruz+"folha-pagamentos/servidoresAtivos?ano=2021"+servidor+mes
# url = urlSerra+servidor
print(url)
# html = requests.get(urlCalumbi).content

chrome_options = Options()
## faz com que o browser não abra durante o processo
chrome_options.add_argument("--headless")
## caminho para o seu webdriver
p = ""
driver = webdriver.Chrome(p +'chromedriver.exe', options=chrome_options)
driver.get(url)
html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')
tabela = soup.find("table", id="table")

print(tabela)