from django.conf.urls import patterns, url

from postings import views

urlpatterns = patterns('',
    url(r'^$', views.Feed.as_view(),
        name='feed',),
    url(r'^create$', views.Create.as_view(),
        name='create',),
)
