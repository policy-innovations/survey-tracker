from django.db.models import Q

from django.contrib import admin

from mptt.admin import MPTTModelAdmin
from main.models import *

from accounts.admin import ObjectPermissionInline, ObjectPermissionMixin

class ProjectAdmin(ObjectPermissionMixin, admin.ModelAdmin):
    inlines = [ObjectPermissionInline]

class RoleInline(admin.TabularInline):
    model = Role
    extra = 2

class RoleAdmin(MPTTModelAdmin):
    list_display = ['name', 'user', 'level', 'get_root',]
    list_filter = ['user', 'project', 'level']
    MPTT_ADMIN_LEVEL_INDENT = 20

    inlines = [RoleInline]

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

    def get_readonly_fields(self, request, obj=None):
        fields = list(super(RoleAdmin, self).get_readonly_fields(request,
                                                                 obj))
        if (not request.user.is_superuser) and request.user==obj.user:
                fields += ['head', 'user', 'project']
        return tuple(fields)

    def get_form(self, request, obj=None):
        form = super(RoleAdmin, self).get_form(request, obj)
        if not request.user.is_superuser:
            #Filter form querysets here
            pass
        return form

class ErrorTypeAdmin(MPTTModelAdmin):
    list_display = ['name', 'level', 'parent', 'get_descendant_count',
                    'get_root',]
    MPTT_ADMIN_LEVEL_INDENT = 20

class UIDStatusAdmin(admin.ModelAdmin):
    list_display = ['uid', 'project', 'all_responsible_people']
    filter_horizontal = ('responsibles',)

admin.site.register(Project, ProjectAdmin)
admin.site.register(ErrorType, ErrorTypeAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(UIDStatus, UIDStatusAdmin)
