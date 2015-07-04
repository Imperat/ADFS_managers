from django.shortcuts import render, loader, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from models import Player, Team
# Create your views here.
def player(request, id):
    template = loader.get_template('player.html')
    players = get_object_or_404(Player, pk=id)
    context = RequestContext(request, {
        'player': players,
    })
    return HttpResponse(template.render(context))

def team(request, id):
    template = loader.get_template('team.html')
    teams = get_object_or_404(Team, pk=id)
    context = RequestContext(request, {
        'team': teams,
    })
    return HttpResponse(template.render(context))
