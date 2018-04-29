from django.conf.urls import url

from ADFS.api import views

api_patterns = [
    url(r'users/$', views.UserList.as_view(), name='users_list'),
]
