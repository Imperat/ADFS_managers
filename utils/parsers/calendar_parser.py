#!/usr/bin/env python
# -*- coding: utf-8 -*-

def parse_calendar(filename):
    calendar = open('./utils/parsers/datas/primary_2014.txt', 'r')

    tour,res = 0, []

    for line in calendar:
        if 'тур' in line:
            tour = line.split(' ')[0]
        teams = line.split(' - ')
        if len(teams) > 1:

            res.append([tour, teams[0], teams[1][0:-1]])

    return res

def add_data():
    a = parse_calendar('kefic')
    from teamlogic.models import MatchInLeague, Team
    for line in a:
        home = Team.objects.filter(name=line[1].capitalize())
        away = Team.objects.filter(name=line[2].capitalize())

        if len(home) > 0:
            home = home[0]
        else:
            print('can not find home team! <<%s>>' % line[1].capitalize())
            continue

        if len(away) > 0:
            away = away[0]
        else:
            print ('can not find away team! <<%s>>' % line[2].capitalize())
            continue

        print('add data: (%s, %s, %s)' %(home, away, line[0]))
        print(home, away, 'RASIM', int(line[0]))
        MatchInLeague.objects.create(
            league_id=8, home=home, away=away, tour=int(line[0]))
