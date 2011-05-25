from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

class Project(models.Model):
    name = models.CharField(_('name'), max_length=100)

    def __unicode__(self):
        return self.name.title()

class Role(MPTTModel):
    '''
    This will generate a hierarchy of people according to their
    posts.
    '''
    name = models.CharField(_('name'), max_length=100)
    head = TreeForeignKey('self', null=True, blank=True,
                          related_name='subordinate')
    project = models.ForeignKey(Project)

    class MPTTMeta:
        order_insertion_by = ['name']
        parent_attr = 'head'

    def __unicode__(self):
        return self.name.title()

class ErrorType(MPTTModel):
    '''
    Possible errors which can occur in the survey. These are nested. An
    error could have multiple suberrors to be choosen from.
    '''
    name = models.CharField(_('name'), max_length=100)
    parent = TreeForeignKey('self', null=True, blank=True,
                             related_name='suberrors')

    class MPTTMeta:
        order_insertion_by = ['name']
        parent_attr = 'parent'

    def __unicode__(self):
        return 'Error type: %s' %(self.name.title())

class UIDStatus(models.Model):
    '''
    This will be table storing the uids from excel exported sheets, linked
    to the db pks.
    '''
    uid = models.CharField(_('unique identifier'), max_length=30,
                           unique=True)
    #The people who are responsible for this survey uid.
    errors = models.ManyToManyField(ErrorType, null=True, blank=True,
                                    through='UIDError')
    responsibles = models.ManyToManyField(Role,
                                          verbose_name=_('responsible people'),
                                          )
    project = models.ForeignKey(Project)

    class Meta:
        verbose_name =  _('UID  status')
        verbose_name_plural=_('UID statuses')

    def __unicode__(self):
        return self.uid

class UIDError(models.Model):
    '''
    An error for a uid - error M2M will be created through this.
    It is where detail is to be defined
    '''
    etype = models.ForeignKey(ErrorType)
    uid_status = models.ForeignKey(UIDStatus)
    details = models.TextField(_('details'), blank=True,
                               help_text="enter extra details which  will\
                               let the error make sense.") #Revise this

#For quick creation of fixtures.

def create_base_role_tree():
    project = Project.objects.get(pk=1)
    superhead = Role.objects.create(name='A', project=project)
    s1 = Role.objects.create(name='B', head=superhead, project=project)
    s2 = Role.objects.create(name='C', head=superhead, project=project)
    ss1 = Role.objects.create(name='D', head=s1, project=project)
    ss2 = Role.objects.create(name='E', head=s1, project=project)
    ss3 = Role.objects.create(name='F', head=s1, project=project)
    ss4 = Role.objects.create(name='G', head=s2, project=project)
    sss1 = Role.objects.create(name='H', head=ss1, project=project)
    sss2 = Role.objects.create(name='I', head=ss3, project=project)
    sss3 = Role.objects.create(name='J', head=ss4, project=project)
    sss4 = Role.objects.create(name='K', head=ss4, project=project)

