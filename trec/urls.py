from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings

from trec import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^about/$', views.about, name='about'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^profile/$', views.profile, name='profile'),
                       url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
                       url(r'^task/(?P<task_id>\d+)/submit/$', views.submit_run, name='submit_run'),
                       url(r'^tracks/$', views.tracks, name="tracks"),
                       url(r'^track/(?P<track_slug>.+)/$', views.track, name='track'),
                       url(r'^add_track', views.add_track, name="add_track"),
                       url(r'^task/(?P<task_id>\d+)/results/$', views.task_results, name="task_results"),
                       url(r'^researchers/$', views.researchers, name='researchers'),
                       url(r'^researcher/(?P<researcher_id>.+)/$', views.researcher, name="researcher"),
)

# had to remove the ^ at the start of media to get it to work on my computer - James
if settings.DEBUG :
    urlpatterns += patterns('',
        (r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )