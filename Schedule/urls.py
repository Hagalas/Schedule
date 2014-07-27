from django.conf.urls import patterns, include, url
from django.contrib import admin
from filebrowser.sites import site
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^download/(?P<file_id>\w+)/$', 'downloader.views.download', name='download'),
    url(r'^parse/(?P<file_id>\w+)/$', 'downloader.views.parse', name='parse'),

    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

)


if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
) + urlpatterns