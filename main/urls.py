from django.conf.urls.defaults import patterns, url

from main.models import * 
urlpatterns = patterns('',
        url(r'^$', 'main.views.home', name = 'home'),
        url(r'^new-entry/$', 'main.views.new_entry', name = 'new_entry'),
        url(r'^get-error-types/$', 'main.views.get_error_types', name = 'get_error_types'),
)
