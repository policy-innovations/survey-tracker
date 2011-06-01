from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name = 'home'),
    #url(r'^new-entry/$', 'main.views.new_entry', name = 'new_entry'),
    url(r'^select-surveyor/(?P<proj_pk>\d+)/$', 'main.views.select_surveyor',
        name = 'select-surveyor'),
    url(r'^add-completed-entry/(?P<role_id>\d+)/$', 'main.views.add_completed_entry',
        name = 'add-completed-entry'),
    url(r'^manage-uids/(?P<role_id>\d+)/$', 'main.views.manage_uids',
        name = 'manage-uids'),
    url(r'^get-error-types/$', 'main.views.get_error_types',
        name = 'get_error_types'),
)
