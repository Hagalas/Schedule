from django.conf.urls import patterns, include, url
from django.contrib import admin
from filebrowser.sites import site
from main.views import GroupListView, GroupDetailView
from django.conf import settings
admin.autodiscover()

from tastypie.api import Api
from main.api.resources import RoomResource
from main.api.resources import SubjectResource
from main.api.resources import FacultyResource
from main.api.resources import GroupResource
from main.api.resources import TeacherResource
from main.api.resources import ScheduleResource

v1_api = Api(api_name='v1')
v1_api.register(RoomResource())
v1_api.register(SubjectResource())
v1_api.register(FacultyResource())
v1_api.register(GroupResource())
v1_api.register(TeacherResource())
v1_api.register(ScheduleResource())


urlpatterns = patterns('',

    url(r'^download/(?P<file_id>\w+)/$', 'downloader.views.download', name='download'),
    url(r'^parse/(?P<file_id>\w+)/$', 'downloader.views.parse', name='parse'),
    url(r'^choose-group/$', GroupListView.as_view(), name='choose-group'),
    url(r'^groups/(?P<pk>[-_\w]+)/$', GroupDetailView.as_view(), name='group-detail'),

    (r'^api/', include(v1_api.urls)),

    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

)


if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
) + urlpatterns