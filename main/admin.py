from django.db.models import Q

from django.contrib import admin

from mptt.admin import MPTTModelAdmin
from main.models import *

from accounts.admin import ObjectPermissionInline, ObjectPermissionMixin

class ProjectAdmin(ObjectPermissionMixin, admin.ModelAdmin):
    inlines = [ObjectPermissionInline]

class RoleAdmin(MPTTModelAdmin):
    list_display = ['name', 'user', 'level', 'head', 'get_root',]
    list_filter = ['user', 'project', 'level']
    MPTT_ADMIN_LEVEL_INDENT = 20

    def queryset(self, request, *args, **kwargs):
        qs = super(RoleAdmin, self).queryset(request, *args, **kwargs)
        if request.user.is_superuser:
            return qs
        else:
            self_roles = qs.filter(user=request.user)
            query = Q()
            for role in self_roles:
                left = role.lft
                right = role.rght
                #Filter roles which are under the logged in user
                q = Q(tree_id=role._mpttfield('tree_id'),
                      lft__gte=left,
                      rght__lte=right
                      )
                query |= q

            return qs.filter(query)

class ErrorTypeAdmin(MPTTModelAdmin):
    list_display = ['name', 'level', 'parent', 'get_descendant_count',
                    'get_root',]
    MPTT_ADMIN_LEVEL_INDENT = 20


admin.site.register(Project, ProjectAdmin)
admin.site.register(ErrorType, ErrorTypeAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(UIDStatus)
