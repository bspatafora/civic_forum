from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from postings import views

urlpatterns = patterns('',
    url(r'^$', views.Feed.as_view(),
        name='feed',),
    url(r'^create_alert$', views.CreateAlert.as_view(),
        name='create_alert',),
    url(r'^create_posting$', views.CreatePosting.as_view(),
        name='create_posting',),
    url(r'^alert/(?P<pk>\d+)$', views.AlertDetail.as_view(),
        name='alert_detail',),
    url(r'^(?P<pk>\d+)$', views.Detail.as_view(),
        name='detail',),
    url(r'^update_alert/(?P<pk>\d+)$', views.UpdateAlert.as_view(),
        name='update_alert',),
    url(r'^delete_alert/(?P<pk>\d+)$', views.DeleteAlert.as_view(),
        name='delete_alert',),
    url(r'^delete_posting/(?P<pk>\d+)$', views.DeletePosting.as_view(),
        name='delete_posting',),
    url(r'^create_alert_comment$', views.CreateAlertComment.as_view(),
        name='create_alert_comment',),
    url(r'^create_comment$', views.CreateComment.as_view(),
        name='create_comment',),
    url(r'^delete_alert_comment/(?P<pk>\d+)$', views.DeleteAlertComment.as_view(),
        name='delete_alert_comment',),
    url(r'^delete_comment/(?P<pk>\d+)$', views.DeleteComment.as_view(),
        name='delete_comment',),
)
