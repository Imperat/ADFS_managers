__author__ = 'stronger'

from django.conf.urls import url

from . import views
from . import models

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^art/(?P<id>[0-9]+)/$', views.article, name='article'),
]