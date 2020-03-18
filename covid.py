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

# gets stats for world
for header in soup.find_all('h1'):
    if "Coronavirus" in str(header):
        number = header.find_next_sibling()
        covid_stats.append(str(number.get_text()).replace(" ",""))
    elif "Deaths" in str(header):
        number = header.find_next_sibling()
        covid_stats.append(str(number.get_text()).replace(" ", ""))

# gets stats for US
for header in soup2.find_all('h1'):
    if "Coronavirus" in str(header):
        number = header.find_next_sibling()
        covid_stats.append(str(number.get_text()).replace(" ",""))
    elif "Deaths" in str(header):
        number = header.find_next_sibling()
        covid_stats.append(str(number.get_text()).replace(" ", ""))

# collecting table data for Illinois
state_table = soup2.table
table_rows = state_table.find_all('tr')

for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text for i in td]
    if not row: # incase an array is empty so we don't access it in the next elif
        continue
    elif " Illinois " in row[0]:
        covid_stats.append(str(row[1].replace(" ","")))
        covid_stats.append(str(row[3].replace(" ","")))

for elem in covid_stats:
    print(elem)

:q
