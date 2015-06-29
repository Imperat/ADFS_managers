__author__ = 'stronger'

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]