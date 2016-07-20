from teamlogic.models import Player, Stadium

from rest_framework import serializers


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ('firstName', 'lastName', 'birth', 'vk_link')