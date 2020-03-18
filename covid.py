import requests
from bs4 import BeautifulSoup

url = "https://www.worldometers.info/coronavirus/"
url2 = "https://www.worldometers.info/coronavirus/country/us/"

r = requests.get(url)
r2 = requests.get(url2)

# throws an exception when request fails
r.raise_for_status()
r2.raise_for_status()

soup = BeautifulSoup(r.text, 'html.parser')
soup2 = BeautifulSoup(r2.text, 'html.parser')

covid_stats = []

for header in soup.find_all('h1'):
    if "Coronavirus" in str(header):
        number = header.find_next_sibling()
        covid_stats.append(str(number.get_text()).replace(" ",""))
    elif "Deaths" in str(header):
        number = header.find_next_sibling()
        covid_stats.append(str(number.get_text()).replace(" ", ""))

for header in soup2.find_all('h1'):
    if "Coronavirus" in str(header):
        number = header.find_next_sibling()
        covid_stats.append(str(number.get_text()).replace(" ",""))
    elif "Deaths" in str(header):
        number = header.find_next_sibling()
        covid_stats.append(str(number.get_text()).replace(" ", ""))


for elem in covid_stats:
    print(elem)

