from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from datetime import datetime
from itertools import groupby

from utils.helpers import NULLABLE, cmp_to_key

from .api.helpers import parse_time_to_string

class Stadium(models.Model):
    """
    Simple model of stadium.
    """
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    accr = models.BooleanField(default=True)
    description = models.TextField(default="olo")
    estimate = models.FloatField()
    physics = models.IntegerField()
    # Need to add relation to Date and Time free!!!
    home = models.ManyToManyField('Team', **NULLABLE)
    image = models.ImageField(upload_to='media', default='/media/404/')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("stadion", args=(self.id,))


class TimeBoard(models.Model):
    date = models.DateField()
    time1 = models.IntegerField()
    time2 = models.IntegerField()
    match = models.ForeignKey('Match')
    stadion = models.ForeignKey('Stadium')

    def __str__(self):
        return '%s / %s [%s - %s]' % (str(self.match), self.stadion.name,
                                      parse_time_to_string(self.time1),
                                      parse_time_to_string(self.time2))


class Player (models.Model):
    """
    Simple model of player.
    """
    firstName = models.CharField(max_length=70)
    lastName = models.CharField(max_length=70)
    birth = models.DateField()
    vk_link = models.CharField(max_length=30, null=True)
    # G - goalkeeper, H - defender, F - nap
    basePosition = models.CharField(max_length=1)
    image = models.ImageField(upload_to="media", **NULLABLE)
    history = models.ManyToManyField('Team', through='RecOfTeam')

    def __str__(self):
        return "%s %s" % (self.firstName, self.lastName)

    def get_absolute_url(self):
        return reverse("player", args=(self.id,))


class Team(models.Model):
    """
    Simple model of Team.
    """
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    foundation = models.IntegerField()
    image = models.ImageField(upload_to="media", **NULLABLE)
    players = models.ManyToManyField('Player', through='RecOfTeam')
    vk_link = models.CharField(max_length=30, default="nulls", **NULLABLE)
    captain = models.ForeignKey('Player', related_name='+', **NULLABLE)
    home = models.ForeignKey('Stadium', **NULLABLE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("team", args=(self.id,))


class RecOfTeam(models.Model):
    """
    All players can exchange teams times for times.
    We need to store this information. Also in every
    team Player has individual number.
    """
    beginDate = models.DateField(**NULLABLE)
    endDate = models.DateField(**NULLABLE)
    team = models.ForeignKey('Team')
    player = models.ForeignKey('Player')
    number = models.IntegerField(default=-1)

    def __unicode__(self):
        return unicode("%s (%s)" % (self.player.__unicode__(),
                                    self.team.__unicode__()))

    def get_end_date(self):
        if self.endDate.year > datetime.now().year:
            return u"At our time"
        else:
            return self.endDate


class Goal(models.Model):
    """
    Model of goal. Goal has accordings author,
    team of author, type (penalty, no-penalty),
    minuts of match.
    """
    author = models.ForeignKey(Player)
    team = models.ForeignKey(Team, **NULLABLE)
    type = models.CharField(max_length=2)
    min = models.IntegerField(null=True)

    def __unicode__(self):
        return "Goal of %s" % self.author.__unicode__()


class Match(models.Model):
    """
    Simple model of match.
    """
    league = models.ForeignKey('Tournament', default=1, null=True)
    home = models.ForeignKey(Team, related_name='+')
    away = models.ForeignKey(Team, related_name='+')
    home_goal = models.IntegerField()
    away_goal = models.IntegerField()
    home_goal_first = models.IntegerField()
    away_goal_first = models.IntegerField()
    technical = models.BooleanField(default=False)
    place = models.ForeignKey(Stadium)
    date_time = models.DateTimeField(**NULLABLE)
    home_goals = models.ManyToManyField('Goal', related_name='home', **NULLABLE)
    away_goals = models.ManyToManyField('Goal', related_name='away', **NULLABLE)

    hasResult = models.BooleanField(default=False)
    status = models.CharField(max_length=30, **NULLABLE)
    register = models.BooleanField(default=False)

    tour = models.IntegerField(**NULLABLE)

    locked = models.BooleanField(default=False)

    def this_team(self, team):
        """ Has team take competition in Match? """
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
        return reverse("match", args=(self.id,))

    def __str__(self):
        if not self.hasResult:
            return "%s - %s" % (self.home.name, self.away.name)
        return "%s - %s (%i - %i)" % (self.home.name, self.away.name,
                                              self.home_goal, self.away_goal)


class Tournament(models.Model):
    """
    Simple model of football league. If leagues of this type
    there is minimum one match between any two teams from league.
    """
    name = models.CharField(max_length=30)
    begin_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField()
    #And so hard!
    members = models.ManyToManyField(Team, through='TeamInLeague')
    matchs = models.ManyToManyField('MatchInLeague')

    def get_calendar(self):
        """
        It's good idea to have calendar of matches in
        dictinary format with keys are number of tours
        anv values is sets of matches.
        """
        tour_count = max([match.tour for match in self.matchs.all()])
        list_of_matches = []
        for tour in range(1, tour_count+1):
            yield list_of_matchs.append((tour, a.filter(tour=i)))

    def generate_calendar(self):
        """
        If admin of ADFS will create new tournament he just
        must run this method for generate list of matches
        automatically.
        """
        pass  # not Implemented

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

        lst_teams.sort(key=cmp_to_key(a), reverse=True)
        return lst_teams

    def __str__(self):
        return "%s %s" % (self.name, self.get_season())

    def get_season(self):
        a = self.begin_date.year
        b = self.end_date.year
        if a == b:
            return str(a)
        return '%s/%s' % (a, b)

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
            d[0] = {'v': 0, 'n': 1, 'p': 0,
                    'sab': m.home_goal, 'prop': m.away_goal}
            d[1] = {'v': 0, 'n': 1, 'p': 0,
                    'sab': m.away_goal, 'prop': m.home_goal}
        else:
            if m.is_home_winner:
                d[0] = {'v': 1, 'n': 0, 'p': 0,
                        'sab': m.home_goal, 'prop': m.away_goal}
                d[1] = {'v': 0, 'n': 0, 'p': 1,
                        'sab': m.away_goal, 'prop': m.home_goal}
            if m.is_away_winner:
                d[0] = {'v': 0, 'n': 0, 'p': 1,
                        'sab': m.home_goal, 'prop': m.away_goal}
                d[1] = {'v': 1, 'n': 0, 'p': 0,
                        'sab': m.away_goal, 'prop': m.home_goal}
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
        return reverse("league", args=(self.id,))

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
    """
    All matches in league have meta information
    about tour of calendar of this league and
    probably other in future :)
    """
    tour1 = models.IntegerField(default=0)

    def all_team_matches(self, team):
        a = MatchInLeague.objects.all()
        x = []
        for i in a:
            if i.this_team(team):
                x.append(i)
        return x


class TeamInLeague(models.Model):
    """
    Team has many propertyes in league.
    For example points and count of goals.
    """
    team = models.ForeignKey(Team)
    league = models.ForeignKey(Tournament)
    goal_s = models.IntegerField()
    goal_p = models.IntegerField()
    match_v = models.IntegerField()

    match_n = models.IntegerField()
    match_p = models.IntegerField()
    penalty = models.IntegerField(default=0)

    straf = models.IntegerField()

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
