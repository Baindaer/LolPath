# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from .models import *
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'lolpath/index.html'
    context_object_name = 'lastest_summoner_list'

    def get_queryset(self):
        return Summoner.objects.all()


def match_list(request):
    return HttpResponse("You're looking at matches list")


def match_form(request, match_id):
    match_id = Summoner.objects.get(id=match_id)
    context = {
        'match_id': match_id
    }
    return render(request, 'lolpath/match_view.html', context)


