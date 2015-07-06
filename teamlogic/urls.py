__author__ = 'stronger'

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^player/(?P<id>[0-9]+)/$', views.player, name='player'),
    url(r'^team/(?P<id>[0-9]+)/$', views.team, name='team'),
    url(r'team/(?P<id>[0-9]+)/matches/', views.team_matches, name='ind_calendar'),
    url(r'^stadium/(?P<id>[0-9]+)/$', views.stadium, name='stadium'),
    url(r'^match/(?P<id>[0-9]+)/$', views.match, name='match'),
    url(r'^league/(?P<id>[0-9]+)/$', views.league, name='league'),
    url(r'^league/(?P<id>[0-9]+)/calend/$', views.calendar, name='calendar'),
    url(r'^league/(?P<id>[0-9]+)/bomb/$', views.bombardiers, name='bombardiers'),
]
