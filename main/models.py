from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

class Project(models.Model):
    name = models.CharField(_('name'), max_length=100)
    users = models.ManyToManyField(User, blank=True)

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
    user = models.ForeignKey(User)

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
        verbose_name =  _('UID status')
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

def get_dummy_user(username):
    user, new = User.objects.get_or_create(username=username)
    if new:
        user.set_password(username)
        user.save()
    return user

def create_role(name, head=None):
    user = get_dummy_user(name)
    project, new = Project.objects.get_or_create(pk=1)
    if new:
        project.name = 'Base Project'
        project.save()
    project.users.add(user)
    return Role.objects.create(name=name, project=project, user=user,
                               head=head)

def create_base_role_tree():
    superhead = create_role('A')

    r1 = create_role('B', superhead)
    r11 = create_role('D', r1)
    r111 = create_role('H', r11)

    r12 = create_role('E', r1)
    r13 = create_role('F', r1)
    r131 = create_role('I', r13)

    r2 = create_role('C', superhead)
    r21 = create_role('G', r2)
    r211 = create_role('J', r21)
    r212 = create_role('K', r21)
