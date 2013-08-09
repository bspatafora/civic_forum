from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from postings import views

urlpatterns = patterns('',
    url(r'^$', login_required(views.Feed.as_view()),
        name='feed',),
    url(r'^create_posting$', login_required(views.CreatePosting.as_view()),
        name='create_posting',),
    url(r'^(?P<pk>\d+)$', login_required(views.Detail.as_view()),
        name='detail',),
    url(r'^delete_posting/(?P<pk>\d+)$', login_required(views.DeletePosting.as_view()),
        name='delete_posting',),
    url(r'^create_comment$', login_required(views.CreateComment.as_view()),
        name='create_comment',),
    url(r'^delete_comment/(?P<pk>\d+)$', login_required(views.DeleteComment.as_view()),
        name='delete_comment',),
)
