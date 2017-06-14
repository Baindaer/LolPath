from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^match/$', views.match_list, name='match'),
    url(r'^update_champs/$', views.update_champs_req, name='update_champs_req'),
    url(r'^match/(?P<match_id>[0-9]+)/$', views.match_form, name='match_detail'),
]