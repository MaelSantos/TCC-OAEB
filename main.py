from bs4 import BeautifulSoup

import requests

html = requests.get("https://www.climatempo.com.br/").content

soup = BeautifulSoup(html, 'html.parser')

# print(soup.prettify())
# print(soup.span);

# temperatura = soup.find("div", class_="_flex _justify-center _align-center")
# temperatura = soup.find("span", class_="shimmer-placeholder -text -bold -gray-dark-2 -font-55 _margin-l-15")
# temperatura = soup.find("a", class_="actTriggerGA")
# temperatura = soup.findAll("li", class_="item")
temperatura = soup.find("span", id="current-weather-temperature")
# temperatura = soup.find("a", style="font-style:italic;")

print(temperatura)

# soup = BeautifulSoup('<META NAME="City" content="Austin">', 'html.parser')
# soup.find("meta", {"name":"City"})
#
# print(soup.find("meta", {"name":"City"})['content'])
