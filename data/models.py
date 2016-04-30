from django.db import models

# Create your models here.
class Player(models.Model):
    summoner_id = models.CharField(max_length = 25)
    summoner_name = models.CharField(max_length = 60)
    region = models.CharField(max_length = 5)

    def __str__(self):
            return '%s' % (self.summoner_name)
    class Meta:
        unique_together = ('summoner_id', 'region',)

class Champion(models.Model):
    champion_id = models.CharField(max_length = 25)
    champion_name = models.CharField(max_length = 60)
    title = models.CharField(max_length = 60)
    image_full = models.CharField(max_length = 25)
    image_sprite = models.CharField(max_length = 25)

    def __str__(self):
            return '%s' % (self.champion_name)

class PlayerChampionMastery(models.Model):
    summoner = models.ForeignKey(Player)
    champion = models.ForeignKey(Champion)
    points = models.IntegerField(null = True, blank = True)
    #last_updated = models.DateTimeField(null = True, blank = True)
    def __str__(self):
            return '%s - %s = %s' % (self.summoner, self.champion, self.points)

    class Meta:
        unique_together = ('summoner', 'champion',)