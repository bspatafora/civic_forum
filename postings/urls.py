from django.conf.urls import patterns, url

from postings import views

urlpatterns = patterns('',
    url(r'^$', views.Feed.as_view(),
        name='feed',),
    url(r'^create$', views.Create.as_view(),
        name='create',),
    url(r'^(?P<pk>\d+)$', views.Detail.as_view(),
        name='detail',),
    url(r'^delete/(?P<pk>\d+)$', views.Delete.as_view(),
        name='delete',),
)
