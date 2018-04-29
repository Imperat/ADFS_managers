from rest_framework import serializers

from ADFS import models

class ADFSUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ADFSUser
        fields = ('id', 'avatar', 'email', 'first_name', 'last_name', 'get_username')
