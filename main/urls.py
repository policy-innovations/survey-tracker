from django.conf.urls.defaults import patterns, url

from main.models import * 
urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name = 'home'),
)
