# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Summoner(models.Model):
    id = models.IntegerField(primary_key=True)
    profile_icon_id = models.IntegerField()
    name = models.CharField(max_length=64)
    summoner_level = models.IntegerField('Level')
    account_id = models.IntegerField('Account', default=False)
    lolpath_user = models.ForeignKey(User)
    server = models.CharField(max_length=64)


    def __str__(self):
        return self.name


class Champion(models.Model):
    id = models.IntegerField(primary_key=True)
    # El name se tomara desde el campo key de la api.
    name = models.CharField('Nombre', max_length=128)
    lane = models.CharField(max_length=64)

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
        res = "Se crearon {nc} campeones en la base de datos".format(nc=nc)
        return res


class MatchReg(models.Model):
    # required
    summoner_id = models.ForeignKey(Summoner)
    champion_id = models.ForeignKey(Champion)
    lane = models.CharField('Lane', max_length=32)
    win = models.BooleanField(default=False)
    kills = models.IntegerField('Kills')
    deaths = models.IntegerField('Deaths')
    assists = models.IntegerField('Assists')
    match_date = models.DateField('Match date')
    ranked = models.BooleanField('Ranked game')
    gold = models.FloatField('Gold earned')
    level = models.IntegerField('Level reached')
    cs = models.IntegerField('Creep score')
    duration = models.IntegerField('Duration')
    game_type = models.CharField('Game type', default="Normal", max_length=64)
    server = models.CharField('Server', default='la1', max_length=32)

    def match_month(self):
        if self.match_date:
            return self.match_date[0:7]

    def kda(self):
        k, d, a = self.kills, self.deaths, self.assists
        kda = (k + a) / d
        return kda


class ChampReport(models.Model):
    champion_id = models.ForeignKey(Champion)
    lane = models.CharField('Lane', max_length=32)
    time_played = models.IntegerField('Time played')
    kills_avg = models.FloatField('Average kills')
    deaths_avg = models.FloatField('Averege deaths')
    assists_avg = models.FloatField('Average assists')
    games = models.IntegerField('Total games')
    wins = models.IntegerField('Total wins')
    defeats = models.IntegerField('Total loses')
    cs_min = models.FloatField('CS per min')
    gold_min = models.FloatField('Gold per min')
    kda = models.FloatField('KDA ratio')
    performance = models.FloatField('LolPath points')
    summoner_id = models.ForeignKey(Summoner)

