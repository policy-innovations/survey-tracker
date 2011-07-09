import os

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.contrib.admin.widgets import FilteredSelectMultiple
from mptt.forms import TreeNodeChoiceField
from main.models import UIDError, ErrorType, UIDQuestion, UIDStatus, \
        Questionnaire , Question, Choice, Role


class ExtFileField(forms.FileField):
    '''
    Same as forms.FileField, but you can specify a file extension whitelist.
    '''
    def __init__(self, *args, **kwargs):
        ext_whitelist = kwargs.pop("ext_whitelist")
        self.ext_whitelist = [i.lower() for i in ext_whitelist]

        super(ExtFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ExtFileField, self).clean(*args, **kwargs)
        filename = data.name
        ext = os.path.splitext(filename)[1]
        ext = ext.lower()
        if ext not in self.ext_whitelist:
            raise forms.ValidationError("Not allowed filetype!")

class ImportUIDForm(forms.Form):
    '''
    This form is used for importing .xls file
    '''
    file = ExtFileField(label=_('Excel file'), ext_whitelist=('.xls',),
            help_text=_('Supported filetypes: .xls'))

class ErrorForm(forms.ModelForm):
    '''
    This is an error form which is to be filled in for associating errors
    with a UID.
    Call it via ajax for error.

    '''
    etype = TreeNodeChoiceField(label=_('Select Error Type'), initial='', queryset=ErrorType.objects.all(),
            widget=forms.HiddenInput(attrs={'class':'error_types'}))

    class Meta:
        model = UIDError
        exclude = ('uid_status', )

    def __init__(self, role,uid_status=None, *args, **kwargs):
        super(ErrorForm, self).__init__(*args, **kwargs)
        self.uid_status = uid_status
        questionnaire = role.get_questionnaire()
        query = Q()
        # This generates a query which filters trees from error type
        # according to the questionnaire's linked error types
        for et in questionnaire.error_types.all():
            q = Q(lft__gte=et.lft, rght__lte=et.rght)
            query |= q
        self.fields['etype'].queryset = ErrorType.objects.filter(query).order_by('level')

    def clean_etype(self):
        cleaned_data = self.cleaned_data
        try:
            et = cleaned_data['etype']
        except:
            return None #If form is empty in formset, "None" is returned.

        if et.is_leaf_node():
            return self.cleaned_data['etype']
        else:
            raise forms.ValidationError("A leaf node is required.")
    def save(self, force_insert=False, force_update=False, commit=True):
        if self.clean_etype() is None:
            return None
        m = super(ErrorForm, self).save(commit=False)
        m.uid_status = self.uid_status
        if commit:
            m.save()
        return m

class UIDCompleteForm(forms.ModelForm):

    def __init__(self, role, data={}, initial = {}, instance=None, *args, **kwargs):
        self.role = role
        questionnaire = role.get_questionnaire()
        self.uids_set = UIDStatus.objects.filter(questionnaire=questionnaire)

        if data.get('uid', False):
            instance = self.uids_set.get(uid=data['uid'])

        super(UIDCompleteForm, self).__init__(data=data, initial=initial,
                                              instance=instance, *args,
                                              **kwargs)

        self.fields['uid'].queryset = self.uids_set
        self.fields['completer'].queryset = role.get_leafnodes(include_self=True)
        self.fields['completer'].required = True
        for question in questionnaire.question_set.all():
            self.fields[question.field_name] = forms.ModelChoiceField(label=_(question.name),
                                                                      queryset=question.get_choices(),
                                                                      initial=data.get(question.field_name))

    def save(self):
        uid = super(UIDCompleteForm, self).save()

        for question in self.role.get_questionnaire().question_set.all():
            choice = self.cleaned_data[question.field_name]
            #choice = question.choice_set.filter(id=choice_id)
            UIDQuestion.objects.create(uid_status=uid, question=question,
                                               selected_choice=choice)

        return uid

    class Meta:
        model = UIDStatus
        exclude = ('questions', 'questionnaire', 'role', 'extra_details',
                   'errors',)
        widgets = {
        }

    class Media:
        css = {
            'all':['css/jquery-ui-1.8.13.custom.css']
        }
        js = ['js/jquery.formset.min.js',]

class QuestionForm(forms.ModelForm):
    '''
    This is a question form which is to be filled if survey was completed.
    '''
    question = forms.CharField(label=_('Q.'), initial='',
            widget= forms.HiddenInput(attrs={'class':'question',
                'readonly':'readonly'}))
    selected_choice = forms.CharField(label=_('Answer'), initial='',
            widget = forms.Select(attrs={'class':'choice'}))

    class Meta:
        model = UIDQuestion
        exclude = ('uid_status')

    def __init__(self, role, uid_status=None, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.uid_status = uid_status
        questionnaire = role.get_questionnaire()
        questions = questionnaire.get_questions()
        choices = []
        for q in questions:
            for c in q.get_choices():
                choices.append(c)
        self.fields['selected_choice'].queryset = choices

    def clean_question(self):
        cleaned_data = self.cleaned_data
        try:
            c = cleaned_data['question']
            return Question.objects.get(pk=int(c))
        except:
            return None #If form is empty in formset, "None" is returned.

    def clean_selected_choice(self):
        cleaned_data = self.cleaned_data
        try:
            c = cleaned_data['selected_choice']
            return Choice.objects.get(pk=int(c))
        except:
            raise forms.ValidationError('Please select a choice.')


    def save(self, force_insert=False, force_update=False, commit=True):
        if self.clean_question() is None:
            return None
        m = super(QuestionForm(),self).save(commit=False)
        m.uid_status = self.uid_status
        if commit:
            m.save()
        return m


class UIDForm(forms.Form):
    '''
    This form should be used for adding status of uid. Extra date field is
    required.
    '''
    uid = forms.CharField(label="UID", required=True, widget=forms.TextInput(
        attrs={'class':'uid'}))

    def __init__(self, role, date, *args, **kwargs):
        '''
        "date" and "role" will be used while saving the form.
        '''
        self.role = role 
        self.date = date
        super(UIDForm, self).__init__(*args, **kwargs)

    def clean_uid(self):
        cleaned_data = self.cleaned_data
        uid = cleaned_data["uid"]
        try:
            uid_status = UIDStatus.objects.get(uid=uid)
        except:
            raise forms.ValidationError('Invalid UID.')
        if uid_status not in self.role.uids():
            raise forms.ValidationError('This UID was not assigned to this surveyor.')
        elif uid_status.completer is not None:
            raise forms.ValidationError('This UID has already been entered.')
        return self.cleaned_data['uid']

    def save(self, force_insert=False, force_update=False, commit=True):
        try:
            uid_status = UIDStatus.objects.get(uid=self.cleaned_data['uid'])
        except:
            return None
        uid_status.completer = self.role
        uid_status.date = self.date
        if commit:
            uid_status.save()
        return uid_status

class UIDAssignmentForm(forms.Form):
    uids = forms.ModelMultipleChoiceField(queryset=Role.objects.all(),
                                          label=_('Select UIDs'),
                                          required=False,
                                          widget=FilteredSelectMultiple(
                                                    _('UIDs'),
                                                    False,
                                                 ))
    csv = forms.CharField(widget=forms.Textarea, required=False,
                          label=_('Or paste comma separated values here'))

    class Media:
        css = {
            'all':['admin/css/widgets.css',
                   'css/uid-manage-form.css'],
        }
        js = ['/admin/jsi18n/']

    def __init__(self, role, subordinate, *args, **kwargs):
        self.role = role
        self.subordinate = subordinate
        super(UIDAssignmentForm, self).__init__(*args, **kwargs)
        self.fields['uids'].queryset = role.managed_uids().pending().filter(role__in=[role, subordinate])

    def clean_csv(self):
        er_uids = []
        raw_csv = self.cleaned_data['csv'].replace(' ', '')

        # csv contains nothing
        if not raw_csv:
            return
        csv = raw_csv.split(',')
        uids_qs_list = self.fields['uids'].queryset.values_list('uid',
                                                                 flat=True)
        for uid in csv:
            if uid not in uids_qs_list:
                er_uids.append(uid)

        if not er_uids:
            return csv
        else:
            er_uids_str = ', '.join(er_uids)
            raise forms.ValidationError(_('The following UIDs are unacceptable: %s' %(er_uids_str) ))

    def assign(self):
        concerned_uids = self.fields['uids'].queryset

        # Check if any csv is posted first
        if self.cleaned_data['csv']:
            sub_new_uids_list = self.cleaned_data['csv']
            # Get new uids queryset from the list obtained through csv
            sub_new_uids = concerned_uids.filter(uid__in=sub_new_uids_list)
        else:
            # No csv use the select box instead
            sub_new_uids = self.cleaned_data['uids']
            sub_new_uids_list = sub_new_uids.values_list('id', flat=True) if sub_new_uids else None

        if sub_new_uids:
            manager_new_uids = self.role.uidstatuses.exclude(id__in = sub_new_uids_list)
            sub_new_uids.update(role=self.subordinate)
        else:
            manager_new_uids = concerned_uids

        manager_new_uids.update(role=self.role)

class QuestionnaireAdminForm(forms.ModelForm):
    hierarchy = forms.ModelChoiceField(queryset=Role.objects.filter(head__isnull=True))
    error_types = forms.ModelMultipleChoiceField(queryset=ErrorType.objects.filter(parent__isnull=True))

    class Meta:
        model=Questionnaire

    def __init__(self, *args, **kwargs):
        super(QuestionnaireAdminForm, self).__init__(*args, **kwargs)

class QuestionAdminForm(forms.ModelForm):
    field_name = forms.RegexField(label=_("Field Name"), max_length=30, regex=r'^[\w]+$',
        help_text = _("Required. 30 characters or fewer. Letters, digits and _ only."),
        error_messages = {'invalid': _("This value may contain only letters, numbers and _.")})

    class Meta:
        model=Question
