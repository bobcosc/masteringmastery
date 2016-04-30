import requests
from data.models import Player, Champion, PlayerChampionMastery
from datetime import datetime,timedelta
from data.helper import *
import sys
import environ
env = environ.Env()
RIOT_API_KEY = env.str('MASTERY_KEY')
REGION = "na"

def get_masters(region):
    REGION = region
    print("getting challengers")
    r = requests.get('https://'+REGION+'.api.pvp.net/api/lol/'+REGION+'/v2.5/league/master?type=RANKED_SOLO_5x5&api_key='+RIOT_API_KEY)
    
    if r.status_code == 200:
        print(str(r.text.encode("utf-8")))    
        for entry in r.json()['entries']:
            print(entry['playerOrTeamId'])
            print(entry['playerOrTeamName'].encode("utf-8"))
            obj, created = Player.objects.update_or_create(
                 summoner_id=entry['playerOrTeamId'], summoner_name=entry['playerOrTeamName'], region=REGION)

def get_platform_id(region):
    platform = None
    if region == 'na':
        platform = "NA1"

    return platform

def get_mastery_points(id, name, region):
    #https://na.api.pvp.net/championmastery/location/NA1/player/5908/champions?api_key=
    print("getting mastery")
    platformID = get_platform_id(region)
    r = requests.get("https://"+region+".api.pvp.net/championmastery/location/"+platformID+"/player/"+str(id)+"/champions?api_key="+RIOT_API_KEY)
    #r = requests.get("https://na.api.pvp.net/championmastery/location/NA1/player/5908/champions?api_key="+RIOT_API_KEY)
    print(r)
    if r.status_code == 200:        
        for entry in r.json():
            player,created = Player.objects.get_or_create(summoner_id=id, summoner_name=name, region=region)                      
            champion = Champion.objects.get(champion_id=entry['championId'])            
            mastery, created = PlayerChampionMastery.objects.get_or_create(summoner=player,champion=champion, points=entry['championPoints']  )               
            mastery.save()
            print(player)
            print(champion)
            print(mastery)

def get_champions():
    #https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?champData=image&api_key=
    r = requests.get("https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?champData=image&api_key="+RIOT_API_KEY)
    print(r.status_code)
    if r.status_code == 200:
        j = r.json()
        for value in r.json()['data'].items():  
            champion, created = Champion.objects.get_or_create(champion_id=value[1]['id'],champion_name = value[1]['name'],
                                                               title = value[1]['title'],image_full = value[1]['image']['full'],
                                                               image_sprite = value[1]['image']['sprite'])
            #champion.champion_name = value[1]['name']
            #champion.title = value[1]['title']
            #champion.image_full = value[1]['image']['full']
            #champion.image_sprite = value[1]['image']['sprite']
            champion.save()





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

def get_single_player_info(id, region):
    #https://na.api.pvp.net/api/lol/na/v1.4/summoner/5908/name?api_key=
    r = requests.get("https://"+region+".api.pvp.net/api/lol/"+region+"/v1.4/summoner/"+str(id)+"/name?api_key="+RIOT_API_KEY)
    if r.status_code == 200:
        player = Player.objects.get_or_create()

   

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