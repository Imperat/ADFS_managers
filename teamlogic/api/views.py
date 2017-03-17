from . import serializers
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response

from teamlogic import models


import datetime
import json

from django.db.models import Q

# Views for REST-API
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def player_list(request):
    if request.method == 'GET':
        players = models.Player.objects.all()
        serializer = serializers.PlayerSerializer(players, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = serializers.PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def team_list(request):
    if request.method == 'GET':
        teams = models.Team.objects.all()
        serializer = serializers.TeamSerializer(teams, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Hachaton endpoints
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def current_matchs(request):
    if request.method == 'GET':
        now = datetime.datetime.now()
        matches_completed = models.Match.objects.order_by('date_time').filter(
            date_time__gt=now, status='completed')[:5]

        matches_futures = models.Match.objects.order_by('date_time').filter(
            Q(status='live') | Q(status='planned'), date_time__gt=now)[:5]

        all_query = []
        all_query.extend(matches_completed)
        all_query.extend(matches_futures)
        result_matches = []
        for match in all_query:
            team1_id = match.home_id
            team2_id = match.away_id
            result_matches.append({
                'id': match.id,
                'team1': {
                    'id': team1_id,
                    'name': match.home.name,
                },
                'team2': {
                    'id': team2_id,
                    'name': match.away.name,
                },
                'goal1': match.home_goal,
                'goal2': match.away_goal,
                'tour': 1,
                'league': {
                    'id': match.league_id,
                    'name': match.league.name
                },
                'location': {
                    'id': match.place_id,
                    'name': match.place.name
                },
                'status': match.status,
                'date': match.date_time.date().isoformat(),
                'time': match.date_time.time().isoformat()
            })
        return Response(result_matches)


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def calendar(request, id=None):
    if id is None:
        return

    matches = models.Match.objects.filter(league_id=id)
    calendar = {}

    for match in matches: 
        entity = {
            'team1': {
                'id': match.home_id,
                'name': match.home.name
            },
            'team2': {
                'id': match.away_id,
                'name': match.away.name
            },
            'date': match.date_time.isoformat(),
            'goal1': match.home_goal,
            'goal2': match.away_goal,
            'status': match.status
        }
        current_tour = calendar.get(match.tour, [])
        current_tour.append(entity)
        calendar[match.tour] = current_tour

    return Response(calendar)













