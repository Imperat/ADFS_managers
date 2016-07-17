from django.shortcuts import render, loader, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from models import Player, Team, Stadium, Match, Tournament, MatchInLeague
import datetime


# Create your views here.


def player(request, id):
    template = loader.get_template('teamlogic/player.html')
    players = get_object_or_404(Player, pk=id)
    context = RequestContext(request, {
        'player': players,
        'user': request.user,
    })
    return HttpResponse(template.render(context))


def team(request, id):
    template = loader.get_template('teamlogic/team.html')
    teams = get_object_or_404(Team, pk=id)
    context = RequestContext(request, {
        'team': teams,
        'nows': datetime.datetime.today(),
        'user': request.user,
    })
    return HttpResponse(template.render(context))


def stadium(request, id):
    template = loader.get_template('teamlogic/stadium.html')
    stadiums = get_object_or_404(Stadium, pk=id)
    context = RequestContext(request, {
        'stadium': stadiums,
        'user': request.user,
    })
    return HttpResponse(template.render(context))


def match(request, id=1):
    template = loader.get_template('teamlogic/match.html')
    matchs = get_object_or_404(Match, pk=id)
    context = RequestContext(request, {
        'match': matchs,
        'nows': datetime.datetime.now(),
        'user': request.user,
    })
    return HttpResponse(template.render(context))


def league(request, id=1):
    if request.method == "GET":
        form = formes.LoginForm()
        template = loader.get_template('teamlogic/league.html')
        leagues = get_object_or_404(Tournament, pk=id)
        leagues.refresh()
        leagues.filtr_matches()
        context = RequestContext(request, {
            'league': leagues,
            'nows': datetime.datetime.now(),
            'form':form,
            'user': request.user,
        })
        if request.user.is_authenticated():
            print "lalka"
            print request.user
        else:
            print "lolka!"
        return HttpResponse(template.render(context))
    else:
        pass


def calendar(request, id=1):
    template = loader.get_template('teamlogic/calendar.html')
    t = get_object_or_404(Tournament, pk=id)
    t.refresh()
    calend = t.get_calendar()
    context = RequestContext(request, {
        'matches': calend,
        'all_team_matches': Match.objects.all().last().all_team_matches(Team.objects.all().last()),
        'user': request.user,
    })
    return HttpResponse(template.render(context))


def team_matches(request, id=1):
    template = loader.get_template('teamlogic/matches.html')
    t = get_object_or_404(Team, pk=id)
    context = RequestContext(request, {
        'all_team_matches': MatchInLeague.objects.all().last().all_team_matches(t),
        'team': t,
        'user': request.user,
    })
    return HttpResponse(template.render(context))


def bombardiers(request, id=1):
    template = loader.get_template('teamlogic/bombardiers.html')
    t = get_object_or_404(Tournament, pk=id)
    context = RequestContext(request, {
        'all_bombardiers': t.get_bombardiers_table(),
        'league': t,
        'user': request.user,
    })
    return HttpResponse(template.render(context))
