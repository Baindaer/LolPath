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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
        try:
            last_match = MatchReg.objects.filter(champion_id=champion_req).order_by('-match_date')[:1]
            if len(last_match) > 0:
                lane = last_match[0].lane
            else:
                lane = champion_id.lane
        except models.ObjectDoesNotExist:
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
        matches = MatchReg.objects.filter(summoner_id=user_summoner.id).order_by('-id')
    except models.ObjectDoesNotExist:
        matches = False

    page = request.GET.get('page', 1)

    paginator = Paginator(matches, 50)
    try:
        matchs = paginator.page(page)
    except PageNotAnInteger:
        matchs = paginator.page(1)
    except EmptyPage:
        matchs = paginator.page(paginator.num_pages)

    context = {
        'active': 'normal',
        'matchs': matchs,
    }
    return render(request, 'lolpath/match_list.html', context)


def match_form(request, match_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to login')
        return HttpResponseRedirect(reverse('lolpath:login'))
    champions = Champion.objects.all().order_by('name')
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
        if request.POST['submit'] == 'cancel':
            return HttpResponseRedirect(reverse('lolpath:match_list'))

    return render(request, 'lolpath/match_form.html', context)


def match_new(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to login')
        return HttpResponseRedirect(reverse('lolpath:login'))
    champions = Champion.objects.all().order_by('name')

    context = {'match_id': False, 'champions': champions}
    if request.method == 'POST':
        if request.POST['submit'] == 'submit_match' or request.POST['submit'] == 'submit_new':
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
            if 'win' in request.POST:
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
            messages.success(request, 'Match registered successfully')
            if request.POST['submit'] == 'submit_match':
                return HttpResponseRedirect(reverse('lolpath:match_form', args=(new_match.id,)))
            if request.POST['submit'] == 'submit_new':
                context['pre_date'] = match_date
                context['pre_champion'] = champion_req
                context['pre_lane'] = lane
                return render(request, 'lolpath/match_form.html', context)
        if request.POST['submit'] == 'cancel':
            return HttpResponseRedirect(reverse('lolpath:match_list'))
    return render(request, 'lolpath/match_form.html', context)


def profile_view(request, server, summoner_name):
    context = {
        'server': server,
        'summoner_name': summoner_name
    }
    return render(request, 'lolpath/profile.html', context)


def search_profile(request):
    if request.method == 'POST':
        server = request.POST['server']
        summoner = request.POST['summoner']
        if server == 'server':
            messages.error(request, 'You need to set the server')

        return HttpResponseRedirect(reverse('lolpath:match_form', args=(new_match.id,)))

