from django.db import models
from django.db.models import Q, Count
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

class Project(models.Model):
    name = models.CharField(_('name'), max_length=100)
    users = models.ManyToManyField(User, blank=True)

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
        return '%s' %(self.name.title())

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
    #Not using role assigned uids now
    #uids = models.ManyToManyField(UIDStatus, blank=True
                                  #verbose_name=_('uid statuses'),
                                  #related_name=_('responsible people')
                                  #)

    class MPTTMeta:
        order_insertion_by = ['name']
        parent_attr = 'head'

    def __unicode__(self):
        return self.name.title()

    def uids(self):
        '''
        This fetches the list of uids which are under a role's
        responsiblity.
        A role has uids assigned to it or if none is, it will be
        responsible for all uids for which its head is and this
        traverses up the hierarchy tree.

        A Role will have uids from the closest ancestor (or itself) who
        has a set.

        Eg:
        Let this be the tree:
        Project: 300
        A
          B (200)
            D
              G
              H
            E
              I
          C
            F
              J
              K

        Now if only B has some uids asigned, then D, E will have same uid
        sets as B and so would G, H, I.
        The rest will be open for distribution and under everybody's
        (except B subtree's) responsibility.
        '''
        project_uids = self.project.uidstatus_set.all()

        ancestors = self.get_ancestors(include_self=True)
        assigned_ancestors = ancestors.filter(uidstatuses__isnull=False)
        if assigned_ancestors:
            return assigned_ancestors.latest('level').uidstatuses.all()

        return project_uids.filter(role__isnull=True)

    uids.short_description = _('UID Statuses')

class UIDStatus(models.Model):
    '''
    This will be table storing the uids from excel exported sheets, linked
    to the db pks.
    '''
    uid = models.CharField(_('unique identifier'), max_length=30,
                           unique=True)
    #The people who are responsible for this survey uid.
    errors = models.ManyToManyField(ErrorType, null=True, blank=True,
                                    through='UIDError', editable=False)
    project = models.ForeignKey(Project)
    role = models.ForeignKey(Role, blank=True, null=True,
                             verbose_name=_('main responsible person'),
                             related_name='uidstatuses')

    class Meta:
        verbose_name =  _('UID status')
        verbose_name_plural=_('UID statuses')

    def __unicode__(self):
        return self.uid

    def responsible_people(self):
        '''
        TODO: Write this
        '''
        return 'Not yet implemented'


class UIDError(models.Model):
    '''
    An error for a uid - error M2M will be created through this.
    It is where detail is to be defined
    '''
    etype = models.ForeignKey(ErrorType)
    uid_status = models.ForeignKey(UIDStatus, editable=False)
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
