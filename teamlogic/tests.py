from django.test import TestCase

from autofixture import AutoFixture

from teamlogic.models import Match


class TestUtils(object):
    @staticmethod
    def create_match(home_goal, away_goal, home_goal_first=None,
                                          away_goal_first=None):
        home_goal_first = home_goal_first or 0
        away_goal_first = away_goal_first or 0
        fixture_match = AutoFixture(
            Match, generate_fk=True,
            field_values={'home_goal': home_goal,
                          'away_goal': away_goal,
                          'home_goal_first': home_goal_first,
                          'away_goal_first': home_goal_first})
        return fixture_match.create(1)[0]


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
