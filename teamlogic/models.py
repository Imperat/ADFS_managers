from django.db import models
from datetime import datetime
from django.utils import timezone

from itertools import groupby
# Create your models here.


class Stadium(models.Model):
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    accr = models.BooleanField(default=True)
    description = models.TextField(default="olo")
    estimate = models.FloatField()
    physics = models.IntegerField()
    # Need to add relation to Date and Time free!!!
    home = models.ManyToManyField('Team', blank=True, null=True)
    image = models.ImageField(upload_to='media', default='/media/404/')

    def __unicode__(self):
        return unicode(self.name)

    def get_absolute_url(self):
        return "/logic/stadium/%i/" % self.id


class Player (models.Model):
    firstName = models.CharField(max_length=70)
    lastName = models.CharField(max_length=70)
    birth = models.DateField()
    vk_link = models.CharField(max_length=30, null=True)
    # G - goalkeeper, H - defender, F - nap
    basePosition = models.CharField(max_length=1)
    image = models.ImageField(upload_to="media")
    history = models.ManyToManyField('Team', through='RecOfTeam', null=True)

    def __unicode__(self):
        return unicode(self.firstName + " " + self.lastName)

    def get_absolute_url(self):
        return "/logic/player/%i/" % self.id


class Team(models.Model):
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    foundation = models.IntegerField()
    image = models.ImageField(upload_to="media")
    players = models.ManyToManyField('Player', through='RecOfTeam')
    vk_link = models.CharField(max_length=30, default="nulls", null=True)
    captain = models.OneToOneField('Player', related_name='+')
    home = models.ForeignKey('Stadium')

    def __unicode__(self):
        return unicode(self.name)

    def get_absolute_url(self):
        return "/logic/team/%i" % self.id


class RecOfTeam(models.Model):
    beginDate = models.DateField( null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)
    team = models.ForeignKey('Team')
    player = models.ForeignKey('Player')
    number = models.IntegerField(default=-1)

    def __unicode__(self):
        return self.player.__unicode__() + " (" + self.team.__unicode__() + ")"

    def get_end_date(self):
        if self.endDate.year > datetime.now().year:
            return u"At our time"
        else:
            return self.endDate


class Goal(models.Model):
    author = models.ForeignKey(Player)
    team = models.ForeignKey(Team, blank=True, null=True)
    type = models.CharField(max_length=2)
    min = models.IntegerField(null=True)

    def __unicode__(self):
        return self.author.__unicode__() + u'Bob'


class Match(models.Model):
    league = models.ForeignKey('Tournament', default=1, null=True)
    home = models.ForeignKey(Team, related_name='+')
    away = models.ForeignKey(Team, related_name='+')
    home_goal = models.IntegerField()
    away_goal = models.IntegerField()
    home_goal_first = models.IntegerField()
    away_goal_first = models.IntegerField()
    technical = models.BooleanField(default=None)
    place = models.ForeignKey(Stadium)
    date_time = models.DateTimeField()
    home_goals = models.ManyToManyField('Goal', related_name='home')
    away_goals = models.ManyToManyField('Goal', related_name='away')

    hasResult = models.BooleanField(default=False)
    register = models.BooleanField(default=False)

    def this_team(self, team):
        """Has 'team' take competition in Match?"""
        return team in (self.home, self.away)

    def all_team_matches(self, team):
        a = Match.objects.all()
        x = []
        for i in a:
            if i.this_team(team):
                x.append(i)
        return x


    def is_starts(self):
        c = self.date_time - timezone.now()
        c = int(c.total_seconds())
        if c > 4000:
            return -1  # Don't beginn's
        elif c < 0:
            return 1  # HAS a result
        else:
            return 0  # Online

    def ago(self):
        c = self.date_time - timezone.now()
        c = int(c.total_seconds())
        return c/60

    def is_home_winner(self):
        return self.home_goal > self.away_goal

    def is_away_winner(self):
        return self.away_goal > self.home_goal

    def is_drawn(self):
        return self.home_goal == self.away_goal

    def get_absolute_url(self):
        return "/logic/match/%i" % self.id

    def __unicode__(self):
        if self.home_goal >= 0 and self.away_goal >=0:
            return unicode("%s - %s (%i - %i)" % (self.home.name, self.away.name, self.home_goal, self.away_goal))
        else:
            return unicode("%s - %s" % (self.home.name, self.away.name))


class Tournament(models.Model):
    name = models.CharField(max_length=30)
    begin_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField()
    #And so hard!
    members = models.ManyToManyField(Team, through='TeamInLeague')
    matchs = models.ManyToManyField('MatchInLeague')

    def get_calendar(self):
        '''
        :return list of tours. Any tour has list of
        his matches:
        '''
        a = self.matchs.all()
        max_tour = 0
        list_of_matchs = []
        for i in a:
            max_tour = max(max_tour, i.tour)
        for i in range(1, max_tour+1):
            list_of_matchs.append((a.filter(tour=i), i))
        return list_of_matchs

    def teams_iter(self):
        lst_teams = list(self.teaminleague_set.all())

        # Comparator.
        def a(x, y):
            x, y = x.get_points(), y.get_points()
            if x > y:
                return 1
            if x == y:
                return 0
            if x < y:
                return -1

        lst_teams.sort(cmp=a, reverse=True)
        return lst_teams

    def __unicode__(self):
        return unicode(self.name) + " " + unicode(str(self.get_season()))

    def get_season(self):
        a = self.begin_date.year
        b = self.end_date.year
        if a == b:
            return str(a)
        else:
            return str(a) + '/' + str(b)

    def filtr_matches(self):
        matchList = MatchInLeague.objects.all()
        self.matchs = matchList.filter(league=self)

    def refresh(self):
        for i in self.matchs.all():
            if i.hasResult and not i.register:
                self.regist(i)
                i.register = True
                i.save()

    def regist(self, m):
        d = [dict(), dict()]
        if m.is_drawn:
            d[0] = {'v': 0, 'n': 1, 'p': 0, 'sab': m.home_goal, 'prop': m.away_goal}
            d[1] = {'v': 0, 'n': 1, 'p': 0, 'sab': m.away_goal, 'prop': m.home_goal}
        else:
            if m.is_home_winner:
                d[0] = {'v': 1, 'n': 0, 'p': 0, 'sab': m.home_goal, 'prop': m.away_goal}
                d[1] = {'v': 0, 'n': 0, 'p': 1, 'sab': m.away_goal, 'prop': m.home_goal}
            if m.is_away_winner:
                d[0] = {'v': 0, 'n': 0, 'p': 1, 'sab': m.home_goal, 'prop': m.away_goal}
                d[1] = {'v': 1, 'n': 0, 'p': 0, 'sab': m.away_goal, 'prop': m.home_goal}
        for i in self.teaminleague_set.iterator():
            if i.team.name == m.home.name:
                i.match_v += d[0]['v']
                i.match_n += d[0]['n']
                i.match_p += d[0]['p']
                i.goal_s += d[0]['sab']
                i.goal_p += d[0]['prop']
                i.save()
            if i.team.name == m.away.name:
                i.match_v += d[1]['v']
                i.match_n += d[1]['n']
                i.match_p += d[1]['p']
                i.goal_s += d[1]['sab']
                i.goal_p += d[1]['prop']
                i.save()

    def get_absolute_url(self):
        return "/logic/league/%i" % self.id

    def get_bombardiers_table(self):
        t = []
        for i in self.matchs.all():
            t.extend(i.home_goals.all())
            t.extend(i.away_goals.all())
        pass

        def get_autor(goal):
            return goal.autor
        c = groupby(t, key=get_autor)
        k = []
        for i in c:
            l = 0
            team = 0
            for j in i[1]:
                l += 1
                team = j.team
            k.append((i[0], l, team))
        return k


class MatchInLeague(Match):
    tour = models.IntegerField(default=2)

    def all_team_matches(self, team):
        a = MatchInLeague.objects.all()
        x = []
        for i in a:
            if i.this_team(team):
                x.append(i)
        return x


class TeamInLeague(models.Model):
    team = models.ForeignKey(Team)
    league = models.ForeignKey(Tournament)
    goal_s = models.IntegerField()
    goal_p = models.IntegerField()
    match_v = models.IntegerField()

    match_n = models.IntegerField()
    match_p = models.IntegerField()
    penalty = models.IntegerField()

    def get_goal_difference(self):
        return self.goal_s - self.goal_p

    def get_points(self):
        return 3*self.match_v + self.match_n - self.straf

    def get_matches(self):
        return self.match_n + self.match_v + self.match_p

    def __unicode__(self):
        return unicode(self.team)


class Manager(models.Model):
    tournaments = models.ManyToManyField(Tournament)
    #pokals = models.ManyToManyField(Pokals)
    #leagues = .....
    def get_last_match(self, team):
        pass

    def get_succ_match(self, team):
        pass

    def get_history(self, team1, team2):
        pass


# Constants

