from django.conf.urls import patterns, include, url, static
from django.contrib import admin
from django.contrib.auth.models import User
import admin_tools.urls
from django.conf import settings

from rest_framework import routers, serializers, viewsets

from carusele import urls as carusele_urls
from teamlogic import urls as teamlogic_urls
from ADFS import views


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include(admin_tools.urls)),
    url(r'logic/', include(teamlogic_urls)),
    url(r'^login/', views.autorisation),
    url(r'^survey', views.survey),
    url(r'^register_attention/', views.register_attention),
    url(r'^attention/(?P<id>[0-9]+)/', views.view_attention,
        name='attention'),
    url(r'^', include(carusele_urls)),
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework'))
)

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
