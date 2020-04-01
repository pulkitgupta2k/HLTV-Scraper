from htmls import getHTML
import re
from datetime import datetime
from string import digits
from bs4 import BeautifulSoup
from math import floor

url = "https://www.hltv.org/matches/2340578/alternate-attax-vs-endpoint-esea-advanced-season-33-europe"

html = getHTML(url)

soup = BeautifulSoup(html, "html.parser")

maps = []
try:
    for map in soup.findAll('div', {'class': 'mapname'}):
        maps.append(map.text)
except:
    print("No player stats for %s" % (matchID))
    # return []
ctr = 0
masterArray= []
for index,stats in enumerate(soup.findAll("table", {"class": "table totalstats"})):
        if index < 2:
            continue
        else:
            map = maps[floor(ctr)]
            ctr = ctr+0.5
            for players in stats.findAll('tr', {"class": ""}):
                
                playerID_ = players.a['href']
                playerID_ = playerID_[1:]
                playerID_ = playerID_[playerID_.find('/')+1:playerID_.rfind('/')]
                kd = players.find('td',{'class': 'kd text-center'}).text.split('-')
                k = kd[0]
                d = kd[1]
                adr = players.find('td',{'class': lambda x: x and 'adr' in x.split()}).text
                kast = players.find('td',{'class': lambda x: x and 'kast' in x.split()}).text
                kast = kast[:len(kast)-1]
                rating = players.find('td',{'class': lambda x: x and 'rating' in x.split()}).text
                
                stat = []
                stat.append(map)
                stat.append(playerID_)
                stat.append(k)
                stat.append(d)
                stat.append(adr)
                stat.append(kast)
                stat.append(rating)
                # print(stat)
                masterArray.append(stat)
            
print(masterArray)