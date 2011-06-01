from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

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
    user = models.ForeignKey(User)

    class MPTTMeta:
        order_insertion_by = ['name']
        parent_attr = 'head'

    def __unicode__(self):
        return self.name.title()

    def get_project(self):
        return self.get_root().project
    get_project.short_description = _('project')

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
        project = self.get_project()
        project_uids = project.uidstatus_set.all()

        ancestors = self.get_ancestors(include_self=True)
        assigned_ancestors = ancestors.filter(uidstatuses__isnull=False)
        if assigned_ancestors:
            return assigned_ancestors.latest('level').uidstatuses.all()

        return project_uids.filter(role__isnull=True)

    uids.short_description = _('UID Statuses')

class Project(models.Model):
    name = models.CharField(_('name'), max_length=100)
    users = models.ManyToManyField(User, blank=True)
    # This stores the topmost node of the tree whole children form the
    # hierarchy
    hierarchy = models.OneToOneField(Role, blank=True, null=True,
                                     related_name='project')
    # Tree heads of errors which can occur in the project
    error_types = models.ManyToManyField(ErrorType, blank=True, null=True)

    def __unicode__(self):
        return self.name.title()

    def get_leafnodes(self, inc_self=True):
        return self.hierarchy.get_leafnodes(include_self=inc_self)

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
    project = models.ForeignKey(Project)
    role = models.ForeignKey(Role, blank=True, null=True,
                             verbose_name=_('main responsible person'),
                             related_name='uidstatuses')

    # This field name is not a word will be updated as soon as this Q is
    # answered: http://j.mp/j4VDIO
    completer = models.ForeignKey(Role, blank=True, null=True,
                                  verbose_name=_('who did it?'))

    class Meta:
        verbose_name =  _('UID status')
        verbose_name_plural=_('UID statuses')

    def __unicode__(self):
        return self.uid

    def responsible_people(self):
        '''
        Gives the leaf nodes of the tree below a uid-role's nodes or all
        project leaf nodes if none is assigned.
        '''
        if self.role:
            return self.role.get_leafnodes(include_self=True)
        else:
            return self.project.get_leafnodes()


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
    print r1, r11, r111
    print r12, r13, r131
    print r2, r21, r211, r212
