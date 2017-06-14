# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import auth, messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .RiotApi import RiotApi
import lolpath.RiotConst as Const


def init_api(server='la1'):
    return RiotApi(Const.API_KEY, server)


API = init_api()


def index(request):
    return render(request, 'lolpath/index.html', context=None)


def match_list(request):
    return HttpResponse("You're looking at matches list")


def update_champs_req(request):
    api_champ = API.get_static_champions()
    res = Champion.update_champs(api_champ)
    context = {'data': res}
    return render(request, 'lolpath/index.html', context)


def match_form(request, match_id):
    match_id = Summoner.objects.get(id=match_id)
    context = {
        'match_id': match_id
    }
    return render(request, 'lolpath/match_view.html', context)


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
            return HttpResponseRedirect(reverse('lolpath:index'))
        else:
            messages.error(request, 'Autentication error, please check your credentials')
            return HttpResponseRedirect(reverse('lolpath:login'))
    else:
        # Si no es un request tipo POST se renderiza el login
        return render(request, 'lolpath/login.html')


