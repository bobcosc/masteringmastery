from django.shortcuts import render
from data.models import Player, Champion, PlayerChampionMastery
from data.helper import *
from django.views.generic import TemplateView
import collections
from data.serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
# Create your views here.
class IndexView (TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs) 
        #get_masters('na')
        #for summoner in Player.objects.all():
          #  get_mastery_points(summoner.summoner_id, summoner.summoner_name, summoner.region)

        
        #get_champions()
        #sortedData = sorted(data,key=lambda riotplayer: riotplayer.sortPoints, reverse=True )
       # context['summoners'] = Champion.objects.all()
        #context['champions'] = Champion.objects.all().extra(order_by = ['champion_name'])
        #data = {}
        #for champion in Champion.objects.all():
       #     print(champion.champion_id)
      #      data[champion.champion_name.replace(" ", "").replace("'", "")] = PlayerChampionMastery.objects.filter(champion__champion_id=champion.champion_id).order_by('-points')[:5]      
    #        champ = data[champion.champion_name.replace(" ", "").replace("'", "")]
    #        print(champ)
  #      ordered = collections.OrderedDict(sorted(data.items()))
  #      context['data'] = ordered

        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        context['json'] = serializer
        return context

class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class ChampionList(generics.ListCreateAPIView):
    queryset = Champion.objects.all()
    serializer_class = ChampionSerializer

class MasteryList(generics.ListCreateAPIView):
    queryset = PlayerChampionMastery.objects.all()
    serializer_class = PlayerChampionMasterySerializer

    
    