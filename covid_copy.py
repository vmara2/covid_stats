import requests
from bs4 import BeautifulSoup
import tweepy
import datetime
import re

url = "https://www.worldometers.info/coronavirus/"
url2 = "https://www.worldometers.info/coronavirus/country/us/"
url3 = "https://www.lakecountyil.gov/4377/Coronavirus-Disease-2019-COVID-19"

r = requests.get(url)
r2 = requests.get(url2)
r3 = requests.get(url3)
# throws an exception when request fails
r.raise_for_status()
r2.raise_for_status()
r3.raise_for_status()

soup = BeautifulSoup(r.text, 'html.parser')
soup2 = BeautifulSoup(r2.text, 'html.parser')
soup3 = BeautifulSoup(r3.text, 'html.parser')

def getStats():
    # [world cases, world deaths, US cases, US deaths, Illinois cases, Illinois deaths, Lake County cases]
    covid_stats = []

    # gets stats for world
    for header in soup.find_all('h1'):
        if "Coronavirus" in str(header):
            number = header.find_next_sibling()
            covid_stats.append(str(number.get_text()).replace(" ","").replace("\n",""))
        elif "Deaths" in str(header):
            number = header.find_next_sibling()
            covid_stats.append(str(number.get_text()).replace(" ", "").replace("\n",""))

    # gets stats for US
    for header in soup2.find_all('h1'):
        if "Coronavirus" in str(header):
            number = header.find_next_sibling()
            covid_stats.append(str(number.get_text()).replace(" ","").replace("\n",""))
        elif "Deaths" in str(header):
            number = header.find_next_sibling()
            covid_stats.append(str(number.get_text()).replace(" ", "").replace("\n",""))

    # collecting table data for Illinois
    state_table = soup2.table
    table_rows = state_table.find_all('tr')
    # parsing table data for Illinois row
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        if not row: # incase an array is empty so we don't access it in the next elif
            continue
        elif "Illinois" in row[0]: # once we reach Illinois row, append the data
            covid_stats.append(str(row[1].replace(" ","").replace("\n","")))
            covid_stats.append(str(row[3].replace(" ","").replace("\n","")))
    
    # lake county stats
    lc_text = soup3.table.tr.get_text()
    lc_nums = re.findall(r'\d+', lc_text)
    covid_stats.append(lc_nums[-1].replace("u",""))

    for elem in covid_stats:
        print(elem)

    return covid_stats

def main():
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    ACCESS_KEY = ''
    ACCESS_SECRET = ''

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    stats = getStats()
    now = datetime.datetime.now()

    covid_world = ("\n\nWorld cases: " + stats[0] + "\nWorld deaths: " + stats[1])
    covid_us = ("\nUS cases: " + stats[2] + "\nUS deaths: " + stats[3])
    covid_illinois = ("\nIllinois cases: " + stats[4] + "\nIllinois deaths: " + stats[5])
    covid_lc = ("\nLake County cases: " + stats[6])
    tweet = ("COVID-19 STATS\n" + now.strftime("%m-%d-%y %I:%M %p") + covid_world + covid_us + covid_illinois + covid_lc)
    
    api.update_status(tweet)

if __name__ == '__main__':
    main()

