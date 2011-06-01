from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name = 'home'),
    #url(r'^new-entry/$', 'main.views.new_entry', name = 'new_entry'),
    url(r'^add-entry/(?P<proj_pk>\d+)/$', 'main.views.add_entry',
        name = 'add-entry'),
    url(r'^manage-uids/(?P<role_id>\d+)/$', 'main.views.manage_uids',
        name = 'manage-uids'),
    url(r'^manage-uids/(?P<role_id>\d+)/subordinate/(?P<sub_role>\d+)/$',
        'main.views.manage_sub_uids', name = 'manage-sub-uids'),
    url(r'^get-error-types/$', 'main.views.get_error_types',
        name = 'get_error_types'),
    url(r'^get-errors/$', 'main.views.get_errors', name = 'get_errors'),

)
