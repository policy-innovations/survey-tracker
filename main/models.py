from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

class QuerySetManager(models.Manager):

    def get_query_set(self):
        return self.model.QuerySet(self.model)
    def __getattr__(self, name):
        return getattr(self.get_query_set(), name)

    use_for_related_fields = True

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

    def get_questionnaire(self):
        return self.get_root().questionnaire
    get_questionnaire.short_description = _('questionnaire')

    def managed_uids(self):
        query = Q(role__in=self.get_children()) | Q(role=self)
        return self.get_questionnaire().uidstatus_set.filter(query)

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
        Questionnaire: 300
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
        questionnaire = self.get_questionnaire()
        questionnaire_uids = questionnaire.uidstatus_set.all()

        ancestors = self.get_ancestors(include_self=True)
        # Get all uids which are either assigned to any of ancestors
        # or to no one
        query =  Q(role__in=ancestors) | Q(role__isnull=True)
        return questionnaire_uids.filter(query)

    def uids_count(self):
        return self.uids().count()

class Questionnaire(models.Model):
    name = models.CharField(_('name'), max_length=100)
    users = models.ManyToManyField(User, blank=True)
    # This stores the topmost node of the tree whole children form the
    # hierarchy
    hierarchy = models.OneToOneField(Role, blank=True, null=True,
                                     related_name='questionnaire')
    # Tree heads of errors which can occur in the questionnaire
    error_types = models.ManyToManyField(ErrorType, blank=True, null=True)

    def __unicode__(self):
        return self.name.title()

    def get_descendants(self):
        return self.hierarchy.get_descendants(include_self=True)

    def get_leafnodes(self, inc_self=True):
        return self.hierarchy.get_leafnodes(include_self=inc_self)

    def get_questions(self):
        return Question.objects.all().filter(questionnaire=self)

    def total_uids(self):
        return self.uidstatus_set.count()

    def done_uids(self):
        return self.uidstatus_set.filter(completer__isnull=False).count()

    def completion(self):
        return 100 * self.done_uids()/self.total_uids() if self.total_uids() else 0

class Question(models.Model):
    '''
    Extra multiple choice question to be asked if survey was completed.
    For example -
    Question - What was child's age?
    Choices -
    1. 3
    2. 4
    3. 5
    '''
    name = models.CharField(_('name'), max_length=100)
    field_name = models.CharField(_('field_name'), max_length=40)
    questionnaire = models.ForeignKey(Questionnaire)

    def __unicode__(self):
        return '%s' %(self.name)

    def get_choices(self):
        return self.choice_set.all()

class Choice(models.Model):
    name = models.CharField(_('name'), max_length=100)
    question = models.ForeignKey(Question)

    def __unicode__(self):
        return '%s' %(self.name.title())

class UIDStatus(models.Model):
    '''
    This will be table storing the uids from excel exported sheets, linked
    to the db pks.
    '''
    uid = models.CharField(_('unique identifier'), max_length=30,
            unique=True)
    extra_details = models.TextField(_('extra details'), blank=True)
    #The people who are responsible for this survey uid.
    errors = models.ManyToManyField(ErrorType, null=True, blank=True,
                                    through='UIDError')
    questions = models.ManyToManyField(Question, null=True, blank=False,
            through='UIDQuestion')
    questionnaire = models.ForeignKey(Questionnaire)
    role = TreeForeignKey(Role, blank=True, null=True,
                             verbose_name=_('main responsible person'),
                             related_name='uidstatuses')

    # This field name is not a word will be updated as soon as this Q is
    # answered: http://j.mp/j4VDIO
    completer = models.ForeignKey(Role, blank=True, null=True,
            verbose_name=_('who did it?'))
    date = models.DateField(_('date of completion'), blank=True, null=True)

    objects = QuerySetManager()

    class Meta:
        verbose_name =  _('UID')

    class QuerySet(QuerySet):
        def pending(self):
            return self.filter(completer__isnull=True)

    def __unicode__(self):
        role = self.role.user if self.role else 'Unassigned'
        return '%s - %s' %(self.uid, role)

    def user(self):
        return self.role.user

    def done(self):
        return True if self.completer else False
    done.boolean = True

    def responsible_people(self):
        '''
        Gives the leaf nodes of the tree below a uid-role's nodes or all
        questionnaire leaf nodes if none is assigned.
        '''
        if self.role:
            return self.role.get_leafnodes(include_self=True)
        else:
            return self.questionnaire.get_leafnodes()


class UIDError(models.Model):
    '''
    An error for a uid - error M2M will be created through this.
    It is where detail is to be defined
    '''
    etype = models.ForeignKey(ErrorType)
    uid_status = models.ForeignKey(UIDStatus)
    details = models.TextField(_('error details'), blank=True,
                               help_text="enter extra details just in case\
                               useful.") #Revise this

class UIDQuestion(models.Model):
    '''
    A question for a completed will be created through this.
    '''
    question = models.ForeignKey(Question)
    uid_status = models.ForeignKey(UIDStatus)
    selected_choice = models.ForeignKey(Choice)

#For quick creation of fixtures.

def get_dummy_user(username):
    user, new = User.objects.get_or_create(username=username)
    if new:
        user.set_password(username)
        user.save()
    return user

def create_role(name, head=None, username=None):
    if username:
        user = get_dummy_user(username)
    else:
        user = get_dummy_user(name)

    return Role.objects.get_or_create(name=name, user=user, head=head)[0]

def create_base_role_tree():
    superhead = create_role('A', username='test')

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

    questionnaire, new = Questionnaire.objects.get_or_create(pk=1)
    if new:
        questionnaire.name = 'TestQS'
        questionnaire.save()
    questionnaire.hierarchy = superhead
    questionnaire.save()

    print superhead
    print r1, r11, r111
    print r12, r13, r131
    print r2, r21, r211, r212
    print questionnaire
