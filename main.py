from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests

urlTriunfo = "https://triunfo.pe.gov.br"
urlCalumbi = "https://calumbi.pe.gov.br"

servidor = "servidor=joao"

url = urlCalumbi+"/transparencia/folha-pagamentos/servidoresAtivos?ano=2021&"+servidor
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