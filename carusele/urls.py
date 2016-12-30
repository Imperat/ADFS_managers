from django.conf.urls import url

from carusele import views
from carusele import models

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^art/(?P<id>[0-9]+)/$', views.article, name='article'),
]
