from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = patterns('',
    url(r'^$', views.Feed.as_view(),
        name='feed',),
    url(r'^preferences$', views.Preferences.as_view(),
        name='preferences',),
    url(r'^preferences_saved$', views.PreferencesSaved.as_view(),
        name='preferences_saved',),
    url(r'^alerts$', views.Alerts.as_view(),
        name='alerts',),
    url(r'^community_forum$', views.CommunityForum.as_view(),
        name='community_forum',),
    url(r'^events$', views.Events.as_view(),
        name='events',),
    url(r'^local_government$', views.LocalGovernment.as_view(),
        name='local_government',),
    url(r'^political_discussion$', views.PoliticalDiscussion.as_view(),
        name='political_discussion',),
    url(r'^volunteering$', views.Volunteering.as_view(),
        name='volunteering',),
    url(r'^create_alert$', views.CreateAlert.as_view(),
        name='create_alert',),
    url(r'^create_posting$', views.CreatePosting.as_view(),
        name='create_posting',),
    url(r'^alert/(?P<pk>\d+)$', views.AlertDetail.as_view(),
        name='alert_detail',),
    url(r'^posting/(?P<pk>\d+)$', views.PostingDetail.as_view(),
        name='posting_detail',),
    url(r'^user/(?P<pk>\d+)$', views.UserDetail.as_view(),
        name='user_detail',),
    url(r'^posting/(?P<posting_pk>\d+)/vote$', views.CastVote.as_view(),
        name='vote',),
    url(r'^posting/(?P<posting_pk>\d+)/vote/(?P<item_type>\w+)/(?P<item_pk>\d+)$', views.CastVote.as_view(),
        name='cast_vote',),
    url(r'^update_alert/(?P<pk>\d+)$', views.UpdateAlert.as_view(),
        name='update_alert',),
    # url(r'^delete_alert/(?P<pk>\d+)$', views.DeleteAlert.as_view(),
        # name='delete_alert',),
    # url(r'^delete_posting/(?P<pk>\d+)$', views.DeletePosting.as_view(),
        # name='delete_posting',),
    url(r'^create_alert_comment$', views.CreateAlertComment.as_view(),
        name='create_alert_comment',),
    url(r'^create_posting_comment$', views.CreatePostingComment.as_view(),
        name='create_posting_comment',),
    # url(r'^delete_alert_comment/(?P<pk>\d+)$', views.DeleteAlertComment.as_view(),
        # name='delete_alert_comment',),
    # url(r'^delete_posting_comment/(?P<pk>\d+)$', views.DeletePostingComment.as_view(),
        # name='delete_posting_comment',),
)
