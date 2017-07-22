import datetime

from django.test import TestCase

from autofixture import AutoFixture

from teamlogic.models import Cup
from teamlogic.models import Match
from teamlogic.models import MatchInLeague
from teamlogic.models import MatchPair
from teamlogic.models import Tournament


class TestUtils(object):
    @staticmethod
    def create_match(home_goal, away_goal,
                     home_goal_first=None, away_goal_first=None):
        home_goal_first = home_goal_first or 0
        away_goal_first = away_goal_first or 0
        fixture_match = AutoFixture(
            Match, generate_fk=True,
            field_values={'home_goal': home_goal,
                          'away_goal': away_goal,
                          'home_goal_first': home_goal_first,
                          'away_goal_first': home_goal_first})
        return fixture_match.create(1)[0]

    @staticmethod
    def create_tournament(beginDate=None, endDate=None):
        beginDate = beginDate or datetime.date(2007, 4, 24)
        endDate = endDate or datetime.date(2010, 4, 22)
        fixture_tournament = AutoFixture(
            Tournament, generate_fk=True,
            field_values={'begin_date': beginDate,
                          'end_date': endDate})
        return fixture_tournament.create(1)[0]

    @staticmethod
    def create_cup(beginDate=None, endDate=None):
        beginDate = beginDate or datetime.date(2007, 4, 25)
        endDate = endDate or datetime.date(2008, 1, 1)
        fixture_cup = AutoFixture(
            Cup, generate_fk=True,
            field_values={'begin_date': beginDate,
                          'end_date': endDate})
        return fixture_cup.create(1)[0]


class TestMatches(TestCase):
    def test_drawn_result(self):
        match = TestUtils.create_match(1, 1, 0, 0)
        self.assertTrue(match.is_drawn())

    def test_home_winner_result_positive(self):
        match = TestUtils.create_match(1, 0, 0, 0)
        self.assertTrue(match.is_home_winner())

    def test_home_winner_result_negative(self):
        match = TestUtils.create_match(0, 1, 0, 0)
        self.assertFalse(match.is_home_winner())

    def test_away_winner_result_positive(self):
        match = TestUtils.create_match(0, 1, 0, 0)
        self.assertTrue(match.is_away_winner())

    def test_away_winner_result_negative(self):
        match = TestUtils.create_match(1, 0, 0, 0)
        self.assertFalse(match.is_away_winner())

    def test_getWinner(self):
        match = TestUtils.create_match(1, 0, 0, 0)
        self.assertEqual(match.getWinner(), match.home)

        match = TestUtils.create_match(0, 1, 0, 0)
        self.assertEqual(match.getWinner(), match.away)

        match = TestUtils.create_match(0, 0, 0, 0)
        self.assertEqual(match.getWinner(), None)

    def test_this_team(self):
        match = TestUtils.create_match(1, 0, 0, 0)
        self.assertTrue(match.this_team(match.home))
        self.assertTrue(match.this_team(match.away))
        other_match = TestUtils.create_match(1, 0, 0, 0)
        self.assertFalse(match.this_team(other_match.home))


class TestTournament(TestCase):
    def test_get_season(self):
        for result, end_year in [('2007/2008', 2008), ('2007', 2007)]:
            tournament = TestUtils.create_tournament(
                beginDate=datetime.date(2007, 4, 22),
                endDate=datetime.date(end_year, 11, 23)
            )
            self.assertEqual(result, tournament.get_season())

class TestMatchPair(TestCase):
    def test_getWinner(self):
        # For two match in pair
        first_match = TestUtils.create_match(1, 0, 0, 0)
        second_match = TestUtils.create_match(2, 0, 0, 0)
        second_match.home = first_match.away
        second_match.away = first_match.home

        pair = MatchPair.objects.create(
            first_match=first_match,
            second_match=second_match,
            cup=TestUtils.create_cup(),
            only_one_match=False,
            is_penalty=False)

        self.assertEqual(pair.getWinner(), second_match.home)
        self.assertEqual(pair.getWinner(), first_match.away)

        # For two match in pair with penalty
        second_match = TestUtils.create_match(1, 0, 0, 0)
        second_match.home = first_match.away
        second_match.away = first_match.home

        pair.second_match = second_match
        pair.first_penalty = 5
        pair.second_penalty = 6

        self.assertEqual(pair.getWinner(), first_match.away)
        self.assertEqual(pair.getWinner(), second_match.home)

        pair.only_one_match = True
        self.assertEqual(pair.getWinner(), first_match.home)

        pair.first_match.away_goal = 1
        self.assertEqual(pair.getWinner(), first_match.away)
        # For one match in pair with penalty

    def test_unicode(self):
        first_match = TestUtils.create_match(1, 0, 0, 0)
        second_match = TestUtils.create_match(2, 0, 0, 0)
        second_match.home = first_match.away
        second_match.away = first_match.home

        pair = MatchPair.objects.create(
            first_match=first_match,
            second_match=second_match,
            cup=TestUtils.create_cup(),
            only_one_match=False,
            is_penalty=False)

        self.assertEqual(unicode('%s - %s' % (first_match.home.name,
                                               second_match.home.name)),
                         pair.__unicode__())
