from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from main.models import *

from accounts.admin import ObjectPermissionInline, ObjectPermissionMixin

class ProjectAdmin(ObjectPermissionMixin, admin.ModelAdmin):
    inlines = [ObjectPermissionInline]

class RoleAdmin(MPTTModelAdmin):
    list_display = ['name', 'level', 'head', 'get_descendant_count',
                    'get_root',]
    MPTT_ADMIN_LEVEL_INDENT = 20

class ErrorTypeAdmin(MPTTModelAdmin):
    list_display = ['name', 'level', 'parent', 'get_descendant_count',
                    'get_root',]
    MPTT_ADMIN_LEVEL_INDENT = 20


admin.site.register(Project, ProjectAdmin)
admin.site.register(ErrorType, ErrorTypeAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(UIDStatus)
