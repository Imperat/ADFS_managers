from django.db.models import Q
from django.shortcuts import loader, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

import datetime

from teamlogic import models
from teamlogic import teamlogic_utils
from utils.mixins import PaginatedViewMixin


def get_calendar(league):
    if league is None:
        return
    matches = models.Match.objects.filter(league_id=league.id)
    calendar = {}

    for match in matches:
        current_tour = calendar.get(match.tour, [])
        current_tour.append(match)
        calendar[match.tour] = current_tour
    return calendar


class TeamLogicMainView(TemplateView):
    template_name = "teamlogic/main.html"

    def get_template_names(self):
        if self.request.is_ajax():
            return ["teamlogic/main_ajax.html"]
        return ["teamlogic/main.html"]


class PlayerDetailView(DetailView):
    model = models.Player
    template_name = 'teamlogic/player.html'


class PlayersListView(ListView):
    model = models.Player
    template_name = 'teamlogic/players.html'


class TeamDetailView(DetailView):
    model = models.Team
    template_name = 'teamlogic/team.html'

    def get_template_names(self):
        if self.request.is_ajax():
            return ["teamlogic/team_ajax.html"]
        return ["teamlogic/team.html"]

    def get_context_data(self, **kwargs):
        context = super(TeamDetailView, self).get_context_data(**kwargs)

        context['last_match'] = teamlogic_utils.get_last_team_match(
            context['team'])

        context['next_match'] = teamlogic_utils.get_next_team_match(
            context['team'])

        return context


class TeamListView(PaginatedViewMixin, ListView):
    model = models.Team
    template_name = 'teamlogic/teams.html'

    def get_template_names(self):
        if self.request.is_ajax():
            return ["teamlogic/teams_ajax.html"]
        return ["teamlogic/teams.html"]


class StadionDetailView(DetailView):
    model = models.Stadium
    template_name = 'teamlogic/stadion.html'
    context_object_name = 'stadion'


class StadionListView(PaginatedViewMixin, ListView):
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
        'form_home': teamlogic_utils.get_team_form(matchs.home, matchs.date_time),
        'form_away': teamlogic_utils.get_team_form(matchs.away, matchs.date_time),
    })

    return HttpResponse(template.render(context))


def get_time(request, id=None):
    template = loader.get_template('base_react.html')
    return HttpResponse(template.render(RequestContext(request, {})))


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
            'nows': 2,
            'calendar': get_calendar(leagues)
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
        ).filter(Q(home=t.pk) | Q(away=t.pk)),
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


class CupsListView(ListView):
    model = models.Cup
    template_name = 'teamlogic/cup_set.html'
    context_object_name = 'cups'


class CupDetailView(DetailView):
    model = models.Cup
    template_name = 'teamlogic/cup.html'
    context_object_name = 'cup'
