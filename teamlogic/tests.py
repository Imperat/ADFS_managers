import datetime

from django.test import TestCase

from autofixture import AutoFixture

from teamlogic.models import Match, MatchInLeague, Tournament


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
