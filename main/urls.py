from django.conf.urls.defaults import patterns, url

from main.models import * 
urlpatterns = patterns('',
        url(r'^$', 'main.views.home', name = 'home'),
        url(r'^new-entry/$', 'main.views.new_entry', name = 'new_entry'),
        url(r'^add-entry/(?P<proj_pk>\d+)/$', 'main.views.add_entry', name = 'add_entry'),
        url(r'^get-error-types/$', 'main.views.get_error_types',
            name = 'get_error_types'),
)
