from django.conf.urls import url

import views


urlpatterns = [
    url(r'^player/(?P<id>[0-9]+)/$', views.player, name='player'),
    url(r'^player/', views.players, name='players'),
    url(r'^team/(?P<id>[0-9]+)/$', views.team, name='team'),
    url(r'team/(?P<id>[0-9]+)/matches/', views.team_matches, name='ind_calendar'),
    url(r'^stadion/(?P<id>[0-9]+)/$', views.stadion, name='stadion'),
    url(r'^stadion/$', views.stadions, name='stadions'),
    url(r'^match/(?P<id>[0-9]+)/$', views.match, name='match'),
    url(r'^league/(?P<id>[0-9]+)/$', views.league, name='league'),
    url(r'^league/(?P<id>[0-9]+)/calend/$', views.calendar, name='calendar'),
    url(r'^league/(?P<id>[0-9]+)/bomb/$', views.bombardiers, name='bombardiers'),
]

api_patterns = [
    url(r'^api/players/$', views.player_list, name='api_players'),
]

urlpatterns += api_patterns
