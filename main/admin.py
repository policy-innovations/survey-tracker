from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from main.models import *

class PersonAdmin(MPTTModelAdmin):
    list_display = ['name', 'level', 'head', 'get_descendant_count',
                    'get_root',]
    MPTT_ADMIN_LEVEL_INDENT = 20

admin.site.register(Person, PersonAdmin)
