from django.conf.urls import patterns, url
from trec import views
from django.conf import settings

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^profile/$', views.profile, name='profile'),
                       url(r'^task/(?P<task_id>\d+)/submit/$', views.submit_run, name='submit_run'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
