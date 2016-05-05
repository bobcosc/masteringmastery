from rest_framework import serializers
from data.models import Player, Champion, PlayerChampionMastery

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player

class ChampionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Champion

class PlayerChampionMasterySerializer(serializers.ModelSerializer):
    summoner = PlayerSerializer()
    champion = ChampionSerializer()

    class Meta:
        model = PlayerChampionMastery
        fields = ("summoner", "champion", "points")
