# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from riot_api import RiotConst, RiotApi


class MatchReg(models.Model):
    # required
    summoner_id = models.ForeignKey(Summoner)
    champion_id = models.ForeignKey(Champion)
    lane = models.CharField('Lane')
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
    game_type = models.CharField('Game type', default="Normal")
    season = models.CharField('Season')
    server_id = models.CharField('Server', default='la1')

    def match_month(self):
        if self.datetime:
            return self.datetime[0:7]

    def kda(self):
        k, d, a = self.kills, self.deaths, self.assists
        kda = (k + a) / d
        return kda


class Summoner(models.Model):
    summoner_id = models.IntegerField('Id')
    profile_icon_id = models.IntegerField()
    name = models.CharField(max_length=64)
    summoner_level = models.IntegerField('Level')
    account_id = models.IntegerField('Account')

    def __str__(self):
        return self.name


class Champion(models.Model):
    champ_id = models.IntegerField('Riot champ ID')
    # El name se tomara desde el campo key de la api.
    name = models.CharField('Nombre')

    def __str__(self):
        return self.name

