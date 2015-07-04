__author__ = 'stronger'

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^player/(?P<id>[0-9]+)/$', views.player, name='player'),
    url(r'^team/(?P<id>[0-9]+)/$', views.team, name='team'),
]
