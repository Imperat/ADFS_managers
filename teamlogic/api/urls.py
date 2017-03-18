from django.conf.urls import url

from teamlogic.api import views


api_patterns = [
    url(r'^api/players/$', views.player_list, name='api_players'),
    url(r'^api/teams/$', views.team_list, name='api_team'),

    url(r'^api/v1/matchs', views.current_matchs, name='api_current_matchs'),
    url(r'^api/v1/league/calendar/(?P<id>[0-9]+)', views.calendar, name='api_calendar'),
    url(r'^api/v1/league/stat/(?P<id>[0-9]+)', views.stat, name='api_stat'),
    url(r'^api/v1/match/(?P<id>[0-9]+)', views.set_date, name='api_set_date')
]
