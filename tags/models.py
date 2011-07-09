from django.db import models
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.utils.translation import ugettext_lazy as _

class Tag(MPTTModel):
    title = models.CharField(_('title'), max_length='50')
    parent = TreeForeignKey('self', verbose_name=_('parent'), null=True,
                            blank=True, related_name='children')

    def __unicode__(self):
        return self.title
