from django.db import models
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey


class Person(MPTTModel):
    name = models.CharField(max_length=100)
    supervisor = TreeForeignKey('self', null=True, blank=True,
                                related_name='subordinate')

    class MPTTMeta:
        order_insertion_by = ['name']
        parent_attr = 'supervisor'

    def __unicode__(self):
        return self.name.title()
