from django.db.models import Q


from datetime import datetime


from teamlogic import models


def get_last_team_match(team):
    last_match = models.Match.objects.order_by(
        'date_time').filter(date_time__lt=datetime.now()).filter(
            Q(home=team.pk) | Q(away=team.pk)).first()

    return last_match


def get_next_team_match(team):
    next_match = models.Match.objects.order_by(
        '-date_time').filter(date_time__gt=datetime.now()).filter(
            Q(home=team.pk) | Q(away=team.pk)).first()

    return next_match


def get_team_form(team, date):
    last_matchs = models.Match.objects.filter(
        Q(home=team.pk) | Q(away=team.pk)).filter(
          date_time__lt=date).order_by(
            'date_time')[:5]

    for m in last_matchs:
        setattr(m, 'result_class', m.get_result_of_team(team))

    return last_matchs
