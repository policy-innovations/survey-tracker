from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

class Person(MPTTModel):
    name = models.CharField(_('name'), max_length=100)
    head = TreeForeignKey('self', null=True, blank=True,
                                related_name='subordinate')

    class MPTTMeta:
        order_insertion_by = ['name']
        parent_attr = 'head'

    def __unicode__(self):
        return self.name.title()

class IdStatus(models.Model):
    uid = models.CharField(_('unique identifier'), max_length=30,
                           unique=True)
    responsibles = models.ManyToManyField(Person,
                                          verbose_name=_('responsible people'),
                                          )
