from django.contrib import admin

from mptt.admin import MPTTModelAdmin
from tags.models import Tag

class TagAdmin(MPTTModelAdmin):
    list_display = ['title', 'level', 'parent', 'get_descendant_count',
                    'get_root',]
    MPTT_ADMIN_LEVEL_INDENT = 20

admin.site.register(Tag, TagAdmin)
