from django.conf.urls import patterns, include, url, static
from django.contrib import admin

from django.conf import settings


from carusele import urls as urls1
from teamlogic import urls as urls2

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'untitled1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^carusele/', include(urls1)),
    url(r'logic/', include(urls2)),
)

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


