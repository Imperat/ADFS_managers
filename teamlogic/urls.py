from django.conf.urls import url

from . import views

from teamlogic.api import urls as api_urls


urlpatterns = []

# players urls
urlpatterns += [
    url(r'^player/(?P<pk>[0-9]+)/$',
        views.PlayerDetailView.as_view(), name='player'),

    url(r'^player/', views.PlayersListView.as_view(), name='players'),
]

# team urls
urlpatterns += [
    url(r'^team/(?P<pk>[0-9]+)/$',
        views.TeamDetailView.as_view(), name='team'),
    url(r'^team/(?P<id>[0-9]+)/matches/',
        views.team_matches, name='ind_calendar'),
    url(r'^team/$', views.TeamListView.as_view(), name='teams'),
]

# stadium urls
urlpatterns += [
    url(r'^stadion/(?P<pk>[0-9]+)/$',
        views.StadionDetailView.as_view(), name='stadion'),
    url(r'^stadion/$', views.StadionListView.as_view(), name='stadions'),
]

# matches urls
urlpatterns += [
    url(r'^match/$', views.MatchListView.as_view(), name='matches'),
    url(r'^match/(?P<id>[0-9]+)/$', views.match, name='match'),
]

# leagues urls
urlpatterns += [
    url(r'^league/$', views.all_league, name='allleague'),
    url(r'^league/(?P<id>[0-9]+)/$', views.league, name='league'),
    url(r'^league/(?P<id>[0-9]+)/calend/$', views.calendar, name='calendar'),
    url(r'^league/(?P<id>[0-9]+)/bomb/$',
        views.bombardiers, name='bombardiers'),
]

# api urls
urlpatterns += api_urls.api_patterns

# common urls
urlpatterns += [
    url(r'', views.TeamLogicMainView.as_view(), name='teamlogic_main')
]
