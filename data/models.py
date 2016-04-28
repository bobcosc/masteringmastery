from django.db import models

# Create your models here.
class Player(models.Model):
    summoner_id = models.CharField(max_length = 25)
    summoner_name = models.CharField(max_length = 60)

class Champion(models.Model):
    champion_id = models.CharField(max_length = 25)
    champion_name = models.CharField(max_length = 60)
    title = models.CharField(max_length = 60)
    image_full = models.CharField(max_length = 25)
    image_sprite = models.CharField(max_length = 25)