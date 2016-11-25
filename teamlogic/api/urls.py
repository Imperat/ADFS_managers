from django.conf.urls import url

from teamlogic.api import views


api_patterns = [
    url(r'^api/players/$', views.player_list, name='api_players'),
]
