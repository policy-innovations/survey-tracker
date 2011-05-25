from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from main.models import *

class RoleAdmin(MPTTModelAdmin):
    list_display = ['name', 'level', 'head', 'get_descendant_count',
                    'get_root',]
    MPTT_ADMIN_LEVEL_INDENT = 20

class ErrorAdmin(MPTTModelAdmin):
    list_display = ['name', 'level', 'parent', 'get_descendant_count',
                    'get_root',]
    MPTT_ADMIN_LEVEL_INDENT = 20

admin.site.register(Project)
admin.site.register(Error, ErrorAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(UIDStatus)
