from htmls import getHTML
import re
from datetime import datetime
from string import digits
from bs4 import BeautifulSoup
from math import floor
from time import sleep

# interval = 0

def getEventNames(eventID):
    html = getHTML("https://www.hltv.org/results?offset=0&event=%s" % (eventID))
    # sleep(interval)
    if html is None:
        print("Failed for %s" % (eventID))
        return []
    # Find the type of event (online, LAN, etc)

    #event name new bs4
    soup = BeautifulSoup(html,'html.parser')
    try:
        event_name = soup.find('div', {'class': 'eventname'}).text
    except:
        return []
    #event type
    try:
        event_type = soup.find('td', {'class': 'location gtSmartphone-only'}).text.strip('\n')
    except:
        return []
    # eventTypes = re.findall('text-ellipsis\">.*<', html)
    # if len(event_type) < 1:
    #     return []

    eventEndDate = re.findall('class="standard-headline">.*<', html)
    # if len(eventTypes) > 0:
    #     eventTypes[0] = (eventTypes[0].replace("text-ellipsis\">", "")).replace("<", "")
    #     f = eventTypes[0].rfind("(")
    #     l = eventTypes[0].rfind(")")
    #     eventTypes[0] = eventTypes[0][f+1:l]
    # else:
    #     eventTypes.append(0)

    # print eventEndDate
    if len(eventEndDate) > 0:
        eventEndDate[0] = (eventEndDate[0].replace("class=\"standard-headline\">", "")).replace("<", "")
    else:
        eventEndDate.append(0)
    # Make an array for pool.map to process
    result = []
    result.append(event_type)
    result.append(event_name)
    result.append(eventEndDate[0])
    result.append(eventID)
    return result


def getMatchEvents(matchID):
    html = getHTML("https://www.hltv.org/matches/%s" % (matchID))
    # sleep(interval)
    if html is None:
        print("Failed for %s" % (matchID))
        return []
    # Find the type of event (online, LAN, etc)
    eventName = re.findall('\"/events/.*/', html)
    if len(eventName) < 1:
        print("Failed %s" % (matchID))
        return []

    # print eventType
    if len(eventName) > 1:
        eventName[0] = (eventName[0].replace("\"/events/", "")).split("/", 1)[0]
    else:
        eventName.append(0)

    # Make an array for pool.map to process
    array = []
    array.append(matchID)
    array.append(eventName[0])
    return array


def getTeams(teamID):
    html = getHTML("https://www.hltv.org/team/%s/a" % (teamID))
    # sleep(interval)
    if html is None:
        print("Failed for %s" % (teamID))
        return []
    # Find the type of event (online, LAN, etc)
    soup = BeautifulSoup(html, 'html.parser')
    try:
        teamName = soup.find("div", {"class": "profile-team-name text-ellipsis"}).text
    except:
        return []
    # teamName = re.findall('<div><span class=\"subjectname\">.*</span><br><i', html)
    # if len(teamName) < 1:
    #     return []
    try:
        teamCountry = soup.find("div", {"class": "team-country text-ellipsis"}).text
    except:
        return[]
    # teamCountry = re.findall('fa fa-map-marker\" aria-hidden=\"true\"></i>.*<', html)
    # if len(teamCountry) < 1:
    #     teamCountry = soup.find("div", {"class": "team-country text-ellipsis"}).text
    #     # teamCountry = re.findall('fa fa-map-marker\" aria-hidden=\"true\"></i>.*</div>', html)
    # if len(teamCountry) < 1:
    #     return []

    # print teamName
    # if len(teamName) > 0:
    #     teamName[0] = (teamName[0].replace("<div><span class=\"subjectname\">", "")).replace("</span><br><i", "")
    # else:
    #     teamName.append(0)

    # print teamCountry
    # if len(teamCountry) > 0:
    #     teamCountry[0] = (teamCountry[0].replace("fa fa-map-marker\" aria-hidden=\"true\"></i> ", "")).split("<", 1)[0]
    # else:
    #     teamCountry.append(0)

    # Make an array for pool.map to process
    array = []
    array.append(teamName)
    array.append(teamCountry)
    array.append(teamID)

    return array


def getMatchInfo(matchID):
    html = getHTML("https://www.hltv.org/matches/%s" % (matchID))
    # sleep(interval)
    if html is None:
        print("Failed for %s" % (matchID))
        return []
    # Search variables data-unix="
    soup = BeautifulSoup(html,'html.parser')
    
    teamIDs = re.findall('src=\"https://static.hltv.org/images/team/logo/.*\" class', html)
    teamNames = re.findall('class=\"logo\" title=\".*\">', html)
    map1 = re.findall('<div class=\"mapname\">.*</div>', html)
    scores=[]
    for scoress in soup.findAll('div', {'class': 'results played'}):
        scores.append(str(scoress))
    # Give up if no team names found
    if len(teamNames) < 1:
        return []

    date = []    
    
    # Find the match date
    date.append(soup.find('div', {'class': 'date'}).text)
    # if len(date) > 0:
    #     date[0] = (date[0].replace("data-unix=\"", "")).replace("\"", "")[:-3]
    #     date[0] = datetime.utcfromtimestamp(int(date[0])).strftime('%Y-%m-%d')
    # else:
    #     date.append(0)
    # Find the Teams respective IDs
    if len(teamIDs) > 0:
        teamIDs[0] = (teamIDs[0].replace("src=\"https://static.hltv.org/images/team/logo/", "")).replace("\" class", "")
        teamIDs[1] = (teamIDs[1].replace("src=\"https://static.hltv.org/images/team/logo/", "")).replace("\" class", "")
    else:
        teamIDs.append(0)

    # Find the map(s) that the match was played on
    if len(map1) == 1:
        map1[0] = (map1[0].replace("<div class=\"mapname\">", "")).replace("</div>", "")
    elif len(map1) > 1:
        for i in range(0, len(map1)):
            map1[i] = (map1[i].replace("<div class=\"mapname\">", "")).replace("</div>", "")
    else:
        map1.append(0)

    # Find the team standing and half sides
    sides = []
    if len(scores) == 1:
        if re.findall('\"t\"|\"ct\"', scores[0])[0] == '\"t\"':
            sides.append("T")
            sides.append("CT")
        else:
            sides.append("CT")
            sides.append("T")
    elif len(scores) > 1:
        for i in range(0, len(scores)):
            try:
                if re.findall('\"t\"|\"ct\"', scores[i])[0] == "\"t\"":
                    sides.append("T")
                    sides.append("CT")
                else:
                    sides.append("CT")
                    sides.append("T")
            except:
                print("HLTV altered score layout for %s" % (matchID))
                return[]
    else:
        return []

    ctr=0
    team_scores = []
    team_h_scores = []

    for m in map1:
        team_scores.append([])
        team_h_scores.append([])

    for fins in soup.findAll('div', {'class': 'results-team-score'}):
        team_scores[floor(ctr)].append(fins.text)
        ctr=ctr+0.5
    
    ctr = 0
    
    for fins in soup.findAll('div', {'class': 'results-center-half-score'}):
        string = fins.text
        string = string.replace(':', ' ')
        string = string.replace(';', ' ')
        string = string.replace('(', ' ')
        string = string.replace(')', ' ')
        string = string.split()
        if(len(string) < 5):
            string.append(0)
            string.append(0)
        for s in string:
            team_h_scores[floor(ctr)].append(s)
        ctr=ctr+1
        
    # Find the scores if there is only one map
    if len(map1) == 1:
        scores[0]
    # Find the scores if there are multiple maps
    elif len(map1) > 1:
        for i in range(0, len(scores)):
            scores[i] = re.findall('\d+', scores[i])
    else:
        scores.append(0)

    for i in range(0, len(scores)):
        # If there was no overtime, make the OT value 0
        if len(scores[i]) == 6:
            scores[i].append(0)
            scores[i].append(0)
        elif len(scores[i]) > 6:
            # Do nothing, because OT scores are already calculated
            pass
        else:
            print("HLTV altered score layout for %s" % (matchID))
            return []

    # Make an array for pool.map to process
    result = []
    if len(map1) > 1:
        for i in range(0, len(scores)):
            # Create a temp array so that each map's stats are each contained in their own array
            tempArray = []
            tempArray.append(date[0])
            tempArray.append(map1[i])
            tempArray.append(teamIDs[0])
            tempArray.append(sides[0])
            tempArray.append(team_scores[i][0])
            tempArray.append(team_h_scores[i][0])
            tempArray.append(team_h_scores[i][2])
            tempArray.append(team_h_scores[i][4])
            tempArray.append(teamIDs[1])
            tempArray.append(sides[1])
            tempArray.append(team_scores[i][1])
            tempArray.append(team_h_scores[i][1])
            tempArray.append(team_h_scores[i][3])
            tempArray.append(team_h_scores[i][5])
            tempArray.append(matchID)
            result.append(tempArray)
    else:
        result.append(date[0])
        result.append(map1[0])
        result.append(teamIDs[0])
        result.append(sides[0])
        result.append(team_scores[0][0])
        result.append(team_h_scores[0][0])
        result.append(team_h_scores[0][2])
        result.append(team_h_scores[0][4])
        result.append(teamIDs[1])
        result.append(sides[1])
        result.append(team_scores[0][1])
        result.append(team_h_scores[0][1])
        result.append(team_h_scores[0][3])
        result.append(team_h_scores[0][5])
        result.append(matchID)
    return result


def getMatchLineups(matchID):
    # Set some vars for later
    html = getHTML("https://www.hltv.org/matches/%s" % (matchID))
    # sleep(interval)
    if html is None:
        print("Failed for %s" % (matchID))
        return []
    playerIDs = re.findall('<a href=\"/player/.*/', html)

    # Give up if no team names found
    if len(playerIDs) < 1:
        print("%s failed, no players detected" % (matchID))
        return []
    for i in range(0, len(playerIDs)):
        playerIDs[i] = (playerIDs[i].split("/"))[2].split("/")[0]
    # print(playerIDs)c
    # print(playerIDs[0:5] + playerIDs[10:15])

    # Make an array for pool.map to process
    if len(playerIDs) > 15:
        players = []
        players.append(playerIDs[0])
        players.append(playerIDs[1])
        players.append(playerIDs[2])
        players.append(playerIDs[3])
        players.append(playerIDs[4])
        players.append(playerIDs[5])
        players.append(playerIDs[6])
        players.append(playerIDs[7])
        players.append(playerIDs[8])
        players.append(playerIDs[9])
        players.append(matchID)
        return players
    else:
        print("HLTV altered lineup layout for %s" % (matchID))
        return []


def getPlayers(playerID):
    html = getHTML("https://www.hltv.org/player/%s/a" % (playerID))
    # sleep(interval)
    if html is None:
        print("Failed for %s" % (playerID))
        return []
    # Find the type of event (online, LAN, etc)
    playerName = re.findall('Complete statistics for.*</a>', html)
    if len(playerName) < 1:
        return []

    playerCountry = re.findall('class=\"flag\" title=\".*\"> ', html)
    if len(playerCountry) < 1:
        return []

    # print teamName
    if len(playerName) > 0:
        playerName[0] = (playerName[0].replace("Complete statistics for ", "")).replace("</a>", "")
    else:
        playerName.append(0)

    # print teamCountry
    if len(playerCountry) > 0:
        playerCountry[0] = (playerCountry[0].replace("class=\"flag\" title=\"", "")).replace("\"> ", "")
        playerCountry[0] = (playerCountry[0].replace("\" itemprop=\"nationality", ""))
    else:
        playerCountry.append(0)

    # Make an array for pool.map to process
    array = []
    array.append(playerName[0])
    array.append(playerCountry[0])
    array.append(playerID)

    return array


def getPlayerStats(matchID):
    html = getHTML("https://www.hltv.org/matches/%s" % (matchID))
    # sleep(interval)
    if html is None:
        print("Failed for %s" % (matchID))
        return []
    soup = BeautifulSoup(html, "html.parser")

    # Get maps
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
                    stat.append(matchID)
                    # print(stat)
                    masterArray.append(stat)
                
    return(masterArray)
