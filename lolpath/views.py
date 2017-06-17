# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from datetime import datetime

from django.contrib import auth, messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models

from .models import *
from .RiotApi import RiotApi
import lolpath.RiotConst as Const


def init_api(server='la1'):
    return RiotApi(Const.API_KEY, server)


API = init_api()


def index(request):
    context = {'active': 'home'}
    return render(request, 'lolpath/index.html', context)


def login(request):
    # Definiendo la funcion iniciar sesion con un requerimiento POST
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Usamos el metodo de autenticar de django para validar la informacion
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Contraseña correcta, se marca el usuario como activo
            auth.login(request, user)
            messages.success(request, 'Login sucessfully')
            user_summoner = Summoner.objects.get(lolpath_user=user.id)
            print("El summoner relacionado con el usuario es {sum_name}".format(sum_name=user_summoner.name))
            return HttpResponseRedirect(reverse('lolpath:index'))
        else:
            messages.error(request, 'Autentication error, please check your credentials')
            print("Error de credenciales")
            return HttpResponseRedirect(reverse('lolpath:login'))
    else:
        # Si no es un request tipo POST se renderiza el login
        return render(request, 'lolpath/login.html')


def update_champs_req(request):
    api_champ = API.get_static_champions()
    res = Champion.update_champs(api_champ)
    messages.success(request, res)
    return render(request, 'lolpath/index.html', context=None)


def get_champion_lane(request):
    if request.method == 'POST':
        champion_req = request.POST.get('champion_id')
        champion_id = Champion.objects.get(id=champion_req)
        lane = champion_id.lane

        data = {'lane': lane}
        return HttpResponse(json.dumps(data), content_type='application/json')
    pass


def match_list(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to login')
        return HttpResponseRedirect(reverse('lolpath:login'))

    user_summoner = Summoner.objects.get(lolpath_user=request.user.id)
    try:
        matches = MatchReg.objects.filter(summoner_id=user_summoner.id)
    except models.ObjectDoesNotExist:
        matches = False

    context = {
        'active': 'normal',
        'matches': matches,
    }
    return render(request, 'lolpath/match_list.html', context)


def match_form(request, match_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to login')
        return HttpResponseRedirect(reverse('lolpath:login'))
    champions = Champion.objects.all()
    try:
        match_id = MatchReg.objects.get(id=match_id)
    except models.ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('lolpath:match_new'))
    context = {'match_id': match_id, 'champions': champions}

    if request.method == 'POST':
        if request.POST['submit'] == 'delete_match':
            match_id.delete()
            user_summoner = Summoner.objects.get(lolpath_user=request.user.id)
            try:
                matches = MatchReg.objects.filter(summoner_id=user_summoner.id)
            except models.ObjectDoesNotExist:
                matches = False

            context = {
                'active': 'normal',
                'matches': matches,
            }
            return render(request, 'lolpath/match_list.html', context)

    return render(request, 'lolpath/match_form.html', context)


def match_new(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to login')
        return HttpResponseRedirect(reverse('lolpath:login'))
    champions = Champion.objects.all()
    context = {'match_id': False, 'champions': champions}
    if request.method == 'POST':
        # Agregando matchreg
        champion_req = request.POST['champion_id']
        champion_id = Champion.objects.get(id=champion_req)
        lane = request.POST['lane']
        match_date = datetime.strptime(request.POST['match_date'], "%Y-%m-%d")
        duration = request.POST['duration']
        kills = request.POST['kills']
        deaths = request.POST['deaths']
        assists = request.POST['assists']
        gold = request.POST['gold']
        cs = request.POST['cs']
        level = request.POST['level']
        summoner_id = Summoner.objects.get(lolpath_user=request.user.id)
        ranked = False
        server = summoner_id.server
        if request.POST['win']:
            win = True
        else:
            win = False

        new_match = MatchReg(
            champion_id=champion_id,
            lane=lane,
            match_date=match_date,
            duration=duration,
            kills=kills,
            deaths=deaths,
            assists=assists,
            gold=gold,
            cs=cs,
            level=level,
            summoner_id=summoner_id,
            ranked=ranked,
            server=server,
            win=win
        )
        new_match.save()
        return HttpResponseRedirect(reverse('lolpath:match_form', args=(new_match.id,)))
    return render(request, 'lolpath/match_form.html', context)

