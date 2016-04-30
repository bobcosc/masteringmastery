from django.contrib import admin
from data.models import Player, Champion, PlayerChampionMastery
# Register your models here.
admin.site.register(Player)
admin.site.register(Champion)
admin.site.register(PlayerChampionMastery)