from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics

from ADFS.models import ADFSUser
from ADFS.api import serializers


class UserList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = ADFSUser.objects.all()
    serializer_class = serializers.ADFSUserSerializer

    def get_queryset(self):
        email = self.kwargs['email']
        if (email):
            return ADFSUser.objects.filter(email=email)

        return ADFSUser.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
