from django.db.models import Q

from django.contrib import admin

from mptt.admin import MPTTModelAdmin
from main.models import ErrorType, Role, Questionnaire, UIDStatus, Choice, \
        Question
from main.forms import QuestionnaireAdminForm, QuestionAdminForm

from accounts.admin import ObjectPermissionInline, ObjectPermissionMixin

class ErrorTypeAdmin(MPTTModelAdmin):
    list_display = ['name', 'level', 'parent', 'get_descendant_count',
                    'get_root',]
    MPTT_ADMIN_LEVEL_INDENT = 20

class RoleInline(admin.TabularInline):
    model = Role
    extra = 2
    #filter_horizontal = ('uids',)

class RoleAdmin(MPTTModelAdmin):
    list_display = ['name', 'get_questionnaire', 'user', 'uids_count', 'level']
    list_filter = ['user', 'level']
    MPTT_ADMIN_LEVEL_INDENT = 20
    #filter_horizontal = ('uids',)
    inlines = [RoleInline]

    def queryset(self, request, *args, **kwargs):
        qs = super(RoleAdmin, self).queryset(request, *args, **kwargs)
        if not request.user.is_superuser:
            self_roles = qs.filter(user=request.user)
            query = Q()
            if self_roles:
                for role in self_roles:
                    left = role.lft
                    right = role.rght
                    #Filter roles which are under the logged in user
                    q = Q(tree_id=role._mpttfield('tree_id'),
                          lft__gte=left,
                          rght__lte=right
                          )
                    query |= q
                    print query
                qs = qs.filter(query)
            else:
                qs = self_roles

        return qs

    def get_readonly_fields(self, request, obj=None):
        fields = list(super(RoleAdmin, self).get_readonly_fields(request,
                                                                 obj))
        if (not request.user.is_superuser) and request.user==obj.user:
                fields += ['head', 'user', 'get_questionnaire']
        return tuple(fields)

    def get_form(self, request, obj=None):
        form = super(RoleAdmin, self).get_form(request, obj)
        if not request.user.is_superuser:
            #Filter form querysets here
            pass
        return form

class QuestionnaireAdmin(ObjectPermissionMixin, admin.ModelAdmin):
    form = QuestionnaireAdminForm
    inlines = [ObjectPermissionInline]

class UIDStatusAdmin(admin.ModelAdmin):
    list_display = ['uid', 'questionnaire', 'user', 'responsible_people', 'done']

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 5

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    form = QuestionAdminForm

admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(ErrorType, ErrorTypeAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(UIDStatus, UIDStatusAdmin)
admin.site.register(Question, QuestionAdmin)
