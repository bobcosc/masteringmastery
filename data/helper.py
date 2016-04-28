import requests


import environ
env = environ.Env()
API_KEY = env.str('RIOT_API_KEY')
REGION = "na"

def get_challengers():


    print("getting challengers")

from data.models import Player
from datetime import datetime,timedelta
from data.helper import *

def getChunksOfDictionaryKeys(dict, size):
    keysList =list(dict.keys())
    ids = []
    chunks=[keysList[x:x+size] for x in range(0, len(keysList), size)]    
    i=0 
    for chunk in chunks:
        
        riot = requests.get('https://'+REGION+'.api.pvp.net/api/lol/na/v1.4/summoner/by-name/'+','.join(chunk)+'?api_key='+RIOT_API_KEY).json()
        #get ids from summoner names       
            
        for entry in riot:        
            print(str(i) + " " +str(dict[entry]))
            i=i+1                
            player = Player.objects.get(riotStandardName = entry)
            #if created:
            #    print(player)
            player.summonerID = riot[entry]['id']
            player.summonerName = riot[entry]['name']
            ids.append(riot[entry]['id'])
            player.save()

    return ids

   

def updateRiotData(dict):
    ids = getChunksOfDictionaryKeys(dict, 40)
    getChunksOfListData(ids,dict,10)
    return

def updateTwitchData(dict):
    twitchNames = list(dict.values())
    chunks=[twitchNames[x:x+100] for x in range(0, len(twitchNames), 100)]
    for chunk in chunks:
        streamers = requests.get('https://api.twitch.tv/kraken/streams?game=League%20of%20Legends&channel='+','.join(chunk)+'&limit=100').json()
                                                                                      
        for stream in streamers['streams']:
            #twitchPlayer = TwitchPlayer(sum[0]['channel']['name'],sum[0]['channel']['display_name'], sum[0]['preview']['large'],sum[0]['channel']['url'],sum[0]['channel']['logo'],sum[0]['viewers'])
            players = Player.objects.filter(twitchName__iexact = stream['channel']['name'])
            for player in players:
                player.twitchDisplayName = stream['channel']['display_name']
                player.previewURL = stream['preview']['large']
                player.channelURL =stream['channel']['url']
                player.logoURL = stream['channel']['logo']
                player.currentViewers = stream['viewers']
                player.lastStream = datetime.now()
                player.save()
            #summonerData = RiotPlayer(key,name ,tier,division,leaguePoints,wins,losses, twitchPlayer)
            #data.append(summonerData)

    return

    

def getChunksOfListData(ids,dict,size):
    chunks=[ids[x:x+size] for x in range(0, len(ids), size)]
    data=[]
    for chunk in chunks:
        playerData = requests.get('https://'+REGION+'.api.pvp.net/api/lol/na/v2.5/league/by-summoner/'+','.join(str(x) for x in chunk)+'/entry?api_key='+RIOT_API_KEY).json()        
        for entry in playerData:
            innerValues = playerData[entry][0]
            player = Player.objects.get(riotStandardName = convertName(innerValues['entries'][0]['playerOrTeamName']))
            player.tier = innerValues['tier'].capitalize()       
            player.division = innerValues['entries'][0]['division']
            player.leaguePoints = innerValues['entries'][0]['leaguePoints']
            player.wins = innerValues['entries'][0]['wins']
            player.losses = innerValues['entries'][0]['losses']
            player.riotStandardName = innerValues['entries'][0]['playerOrTeamName']
            player.save()
            
    return data

def get_online():
    dict = get_girls()
    all = []
    for key,value in dict.items():
        player, created = Player.objects.get_or_create(riotStandardName = convertName(key) )
        player.summonerName = key
        player.twitchName = value
        player.save()
        
    twitchData = updateTwitchData(dict)   
    riotData = updateRiotData(dict)

    return 