from django.conf.urls import url

from . import views

app_name = 'lolpath'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^match/$', views.match_list, name='match_list'),
    url(r'^match/id/(?P<match_id>[0-9]+)/$', views.match_form, name='match_form'),
    url(r'^match/new/$', views.match_new, name='match_new'),
    url(r'^update_champs/$', views.update_champs_req, name='update_champs_req'),
    url(r'^get/champion_lane/$', views.get_champion_lane, name='get_champion_lane'),
]
