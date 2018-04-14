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


class RecOfTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecOfTeam
        fields = ('id', 'beginDate', 'endDate', 'team', 'player', 'number')