# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Summoner(models.Model):
    summoner_id = models.IntegerField('Id')
    profile_icon_id = models.IntegerField()
    name = models.CharField(max_length=64)
    summoner_level = models.IntegerField('Level')
    account_id = models.IntegerField('Account', default=False)

    def __str__(self):
        return self.name


class Champion(models.Model):
    id = models.IntegerField(primary_key=True)
    # El name se tomara desde el campo key de la api.
    name = models.CharField('Nombre', max_length=128)

    def __str__(self):
        return self.name

    @staticmethod
    def update_champs(api_champ):
        nc = 0
        for champ in api_champ['data']:
            try:
                Champion.objects.get(id=api_champ['data'][champ]['id'])
            except:
                new_champ = Champion(
                    id=api_champ['data'][champ]['id'],
                    name=api_champ['data'][champ]['key']
                )
                new_champ.save()
                nc += 1
        print("Se crearon {nc} campeones en la base de datos".format(nc=nc))
        return True


class MatchReg(models.Model):
    # required
    summoner_id = models.ForeignKey(Summoner)
    champion_id = models.ForeignKey(Champion)
    lane = models.CharField('Lane', max_length=32)
    win = models.BooleanField(default=False)
    kills = models.IntegerField('Kills')
    deaths = models.IntegerField('Deaths')
    assists = models.IntegerField('Assists')
    datetime = models.DateTimeField('Match date')
    ranked = models.BooleanField('Ranked game')
    gold = models.IntegerField('Gold earned')
    level = models.IntegerField('Level reached')
    cs = models.IntegerField('Creep score')
    duration = models.DurationField('Duration')
    game_type = models.CharField('Game type', default="Normal", max_length=64)
    season = models.CharField('Season', max_length=64)
    server_id = models.CharField('Server', default='la1', max_length=32)

    def match_month(self):
        if self.datetime:
            return self.datetime[0:7]

    def kda(self):
        k, d, a = self.kills, self.deaths, self.assists
        kda = (k + a) / d
        return kda
