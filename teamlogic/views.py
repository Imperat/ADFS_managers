from django.shortcuts import loader, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

import datetime

from teamlogic import models
from utils.mixins import PaginatedViewMixin


class PlayerDetailView(DetailView):
    model = models.Player
    template_name = 'teamlogic/player.html'


class PlayersListView(ListView):
    model = models.Player
    template_name = 'teamlogic/players.html'


class TeamDetailView(DetailView):
    model = models.Team
    template_name = 'teamlogic/team.html'


class TeamListView(PaginatedViewMixin, ListView):
    model = models.Team
    template_name = 'teamlogic/teams.html'


class StadionDetailView(DetailView):
    model = models.Stadium
    template_name = 'teamlogic/stadion.html'
    context_object_name = 'stadion'


class StadionListView(ListView):
    model = models.Stadium
    template_name = 'teamlogic/stadions.html'


class MatchListView(ListView):
    model = models.Match
    template_name = 'teamlogic/match_set.html'
    context_object_name = 'matches'


def match(request, id=None):
    template = loader.get_template('teamlogic/match.html')
    matchs = get_object_or_404(models.Match, pk=id)
    context = RequestContext(request, {
        'match': matchs,
        'nows': datetime.datetime.now(),
        'user': request.user,
    })
    return HttpResponse(template.render(context))


def all_league(request):
    if request.method == "GET":
        template = loader.get_template('teamlogic/all_leagues.html')
        leagues = models.Tournament.objects.all()
        context = RequestContext(request, {
            'leagues': leagues,
            'user': request.user
        })
    return HttpResponse(template.render(context))


def league(request, id=None):
    if request.method == "GET":
        template = loader.get_template('teamlogic/league.html')
        leagues = get_object_or_404(models.Tournament, pk=id)
        context = RequestContext(request, {
            'league': leagues,
            'nows': datetime.datetime.now(),
        })
    return HttpResponse(template.render(context))


def calendar(request, id=id):
    template = loader.get_template('teamlogic/calendar.html')
    t = get_object_or_404(models.Tournament, pk=id)
    t.refresh()
    calend = t.get_calendar()
    context = RequestContext(request, {
        'matches': calend,
        'all_team_matches': models.Match.objects.all().last(
        ).all_team_matches(models.Team.objects.all().last()),
        'user': request.user,
    })
    return HttpResponse(template.render(context))


def team_matches(request, id=1):
    template = loader.get_template('teamlogic/matches.html')
    t = get_object_or_404(models.Team, pk=id)
    context = RequestContext(request, {
        'all_team_matches': models.MatchInLeague.objects.all(
        ).last().all_team_matches(t),
        'team': t,
        'user': request.user,
    })
    return HttpResponse(template.render(context))


def bombardiers(request, id=1):
    template = loader.get_template('teamlogic/bombardiers.html')
    t = get_object_or_404(models.Tournament, pk=id)
    context = RequestContext(request, {
        'all_bombardiers': t.get_bombardiers_table(),
        'league': t,
        'user': request.user,
    })
    return HttpResponse(template.render(context))
