from . import serializers
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response

from teamlogic import models
from .helpers import cmp_to_key, parse_time

from django.views.decorators.csrf import csrf_exempt

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
def cups_list(request):
    pass


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def stadions(requst):
    stadions = models.Stadium.objects.values('id', 'name')
    return Response(stadions)


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
            date_time__lt=now, status='completed')[:5]

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
            'id': match.id,
            'location': {
                'id': match.place_id,
                'name': match.place.name
            },
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
            'status': match.status,
            'date': match.date_time.date().isoformat(),
            'time': match.date_time.time().isoformat()
        }
        current_tour = calendar.get(match.tour, [])
        current_tour.append(entity)
        calendar[match.tour] = current_tour

    return Response(calendar)


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def stat(request, id=None):
    if id is None:
        return

    def get_points(goal1, goal2, status='home'):
        if goal1 == goal2:
            return 1
        if status == 'away':
            goal1, goal2 = goal2, goal1
        if goal1 > goal2:
            return 3
        return 0

    def is_drawn(goal1, goal2):
        return goal1 == goal2

    def is_home_winner(goal1, goal2):
        return goal1 > goal2

    def is_away_winner(goal1, goal2):
        return goal2 > goal1

    def cmp(record1, record2):
        if record1['points'] > record2['points']:
            return 1
        if record2['points'] > record1['points']:
            return -1
        if record1['goals_positive'] - record1['goals_negative'] > record2['goals_positive'] - record2['goals_negative']:
            return 1
        if record1['goals_positive'] - record1['goals_negative'] < record2['goals_positive'] - record2['goals_negative']:
            return -1
        if record1['goals_positive'] > record2['goals_positive']:
            return 1
        if record1['goals_positive'] < record2['goals_negative']:
            return -1
        return 0

    entityes = {}
    matches = models.Match.objects.filter(league_id=id)
    for match in matches:
        if match.home_id not in entityes.keys():
            result = {
                'id': match.home_id,
                'name': match.home.name,
                'matches': 1 if match.status != 'planned' else 0,
                'points': get_points(match.home_goal, match.away_goal, 'home') if match.status != 'planned' else 0,
                'goals_positive': match.home_goal if match.status != 'planned' else 0,
                'goals_negative': match.away_goal if match.status != 'planned' else 0,
                'wins': is_home_winner(match.home_goal, match.away_goal) if match.status != 'planned' else 0,
                'drawns': is_drawn(match.home_goal, match.away_goal) if match.status != 'planned' else 0,
                'lesion': is_away_winner(match.home_goal, match.away_goal) if match.status != 'planned' else 0
            }
            entityes[match.home_id] = result
        else:
            result = entityes[match.home_id]
            result['matches'] += 1  if match.status != 'planned' else 0
            result['points'] += get_points(match.home_goal, match.away_goal, 'home') if match.status != 'planned' else 0
            result['goals_positive'] += match.home_goal if match.status != 'planned' else 0
            result['goals_negative'] += match.away_goal if match.status != 'planned' else 0
            result['wins'] += is_home_winner(match.home_goal, match.away_goal) if match.status != 'planned' else 0
            result['drawns'] += is_drawn(match.home_goal, match.away_goal) if match.status != 'planned' else 0
            result['lesion'] += is_away_winner(match.home_goal, match.away_goal) if match.status != 'planned' else 0

            entityes[match.home_id] = result


        if match.away_id not in entityes.keys():
            result = {
                'id': match.away_id,
                'name': match.away.name,
                'matches': 1 if match.status != 'planned' else 0,
                'points': get_points(match.home_goal, match.away_goal, 'away') if match.status != 'planned' else 0,
                'goals_positive': match.away_goal if match.status != 'planned' else 0,
                'goals_negative': match.home_goal if match.status != 'planned' else 0,
                'wins': is_away_winner(match.home_goal, match.away_goal) if match.status != 'planned' else 0,
                'drawns': is_drawn(match.home_goal, match.away_goal) if match.status != 'planned' else 0,
                'lesion': is_home_winner(match.home_goal, match.away_goal) if match.status != 'planned' else 0
            }
            entityes[match.away_id] = result
        else:
            result = entityes[match.away_id]
            result['matches'] += 1 if match.status != 'planned' else 0
            result['points'] += get_points(match.home_goal, match.away_goal, 'away') if match.status != 'planned' else 0
            result['goals_positive'] += match.away_goal if match.status != 'planned' else 0
            result['goals_negative'] += match.home_goal if match.status != 'planned' else 0
            result['wins'] += is_away_winner(match.home_goal, match.away_goal) if match.status != 'planned' else 0
            result['drawns'] += is_drawn(match.home_goal, match.away_goal) if match.status != 'planned' else 0
            result['lesion'] += is_home_winner(match.home_goal, match.away_goal) if match.status != 'planned' else 0
            entityes[match.away_id] = result
    res = list(entityes.values())

    res.sort(key=cmp_to_key(cmp), reverse=True)
    print(res)
    return Response(res)


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def set_date(request, id):
    if request.method == 'GET':
        match = models.Match.objects.filter(id=id)[0]
        return Response(
        {
            'id': match.id,
            'location': {
                'id': match.place_id,
                'name': match.place.name
            },
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
            'status': match.status,
            'date': match.date_time.date().isoformat(),
            'time': match.date_time.time().isoformat()
        });
    # test manage!!!!
    data = request.data
    time1, time2 = parse_time(data['time1']), parse_time(data['time2'])

    match = models.Match.objects.filter(id=id)[0]

    if match.locked:
        return Response({'error': 'Match is locked'},
                        status=status.HTTP_400_BAD_REQUEST)

    if match.status in ['completed']:
        return Response({'error': 'Match is status:%s' % match.status},
                        status=status.HTTP_400_BAD_REQUEST)

    date=datetime.datetime.strptime(data['date'], '%Y-%m-%d')

    candidates = models.TimeBoard.objects.filter(
        stadion=data['stadion'],
        date=datetime.datetime.strptime(data['date'], '%Y-%m-%d'))

    for cand in candidates:
        if cand.time1 < time1 and cand.time2 > time1:
            return Response({'error': 'Time is locked1111!'},
                status=status.HTTP_400_BAD_REQUEST)
        if cand.time1 < time2 and cand.time2 > time2:
            return Response({'error': 'Time is locked2222!'},
                status=status.HTTP_400_BAD_REQUEST)
        if cand.time1 == time1 and cand.time2 == time2:
            return Response({'error': 'Time is locked'},
                status=status.HTTP_400_BAD_REQUEST)

    timeBoard = models.TimeBoard(
        date=date,
        stadion=models.Stadium.objects.filter(id=data['stadion'])[0],
        match=match,
        time1=time1,
        time2=time2
    )

    match.date_time = datetime.datetime(date.year, date.month, date.day,
                                       int(data['time1'].split(':')[0]),
                                       int(data['time1'].split(':')[1]))
    match.place = models.Stadium.objects.filter(id=data['stadion'])[0]
    match.status = 'planned'
    match.save()
    timeBoard.save()
    return Response({'sucess': 'sucess'})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def set_status(request, id):
    match = models.Match.objects.filter(id=id)[0]

    if match.locked:
        return Response({'error': 'Match is locked'},
                        status=status.HTTP_400_BAD_REQUEST)

    if match.status in ['live', 'completed']:
        return Response({'error': 'Match is status:%s' % match.status},
                        status=status.HTTP_400_BAD_REQUEST)

    data = request.data
    if data['status'] == 'completed' and match.status != 'live':
        return Response({'error': 'error message'}, status=status.HTTP_400_BAD_REQUEST)

    if data['status'] == 'live' and match.status == 'planned':
        match.status = 'live'
        match.save()
        return Response({'status': 'live'})

    if data['status'] == 'completed' and match.status == 'live':
        match.save()
        return Response({'status': 'completed'})

@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def stadion_times(request, id):
    if request.method == 'GET':
        entityes = models.TimeBoard.objects.filter(stadion_id=id)
        serializer = serializers.TimeBoardSerializer(entityes, many=True)
        return Response(serializer.data)
    new_time = models.TimeBoard(stadion_id=id, time1=request.data['time1'],
        time2=request.data['time2'],
        date=datetime.datetime.strptime(request.data['date'], '%Y-%m-%d'));

    new_time.save()
    return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)
