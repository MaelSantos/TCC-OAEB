# import dryscrape
from bs4 import BeautifulSoup

urlSantaCruz = "https://www.santacruzdabaixaverde.pe.gov.br/transparencia/"
servidor = "&servidor=joao"
mes = "&mes=3"

url = urlSantaCruz+"folha-pagamentos/servidoresAtivos?ano=2021"+servidor+mes
print(url)

from requests_html import HTMLSession

session = HTMLSession()
r = session.get(url)
print(r.html.render())
print(r.html.search('id="table"'))

# session = dryscrape.Session()
# session.visit(url)
# response = session.body()
# soup = BeautifulSoup(response)
#
# tabela = soup.find("table", id="table")
# print(tabela)

