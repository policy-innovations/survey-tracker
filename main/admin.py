from django.contrib import admin
from main.models import *

class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'supervisor', 'get_descendant_count',
                    'get_root',]

admin.site.register(Person, PersonAdmin)
