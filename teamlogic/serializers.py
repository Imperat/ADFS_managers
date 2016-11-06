from rest_framework import serializers

import models


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
        models = models.Stadium
        fields = ('id', 'name', 'city', 'accr', 'description',
                  'estimate', 'physics', 'home', 'image')

