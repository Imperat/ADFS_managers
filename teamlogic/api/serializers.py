from rest_framework import serializers

from teamlogic import models


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Player
        fields = ('id', 'firstName', 'lastName', 'birth', 'vk_link',
                  'basePosition', 'image', 'history')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = ('id', 'name', 'city', 'foundation', 'image',
                  'players', 'vk_link', 'captain', 'home')


class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stadium
        fields = ('id', 'name', 'city', 'accr', 'description',
                  'estimate', 'physics', 'home', 'image')


class TimeBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TimeBoard
        fields = ('id', 'date', 'stadion', 'time1', 'time2', 'match')


class MatchSerializer(serializers.ModelSerializer):
    home = TeamSerializer(many=False, read_only=True)
    away = TeamSerializer(many=False, read_only=True)
    class Meta:
        model = models.Match
        fields = ('id', 'home_goal', 'away_goal', 'home', 'away')


class CupDetailSerialiser(serializers.ModelSerializer):
    first_match = MatchSerializer(many=False, read_only=True)
    second_match = MatchSerializer(many=False, read_only=True)
    class Meta:
        model = models.MatchPair
        fields = ('id', 'first_match', 'second_match', 'next_pair', 'only_one_match')
