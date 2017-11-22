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
