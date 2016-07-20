from django.conf.urls import patterns, include, url, static
from django.contrib import admin
import admin_tools.urls
from django.conf import settings


from carusele import urls as urls1
from teamlogic import urls as urls2
from ADFS import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'untitled1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include(admin_tools.urls)),
    url(r'^carusele/', include(urls1)),
    url(r'logic/', include(urls2)),
    url(r'^login/', views.autorisation),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


