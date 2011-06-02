from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from datetime import date, timedelta
from django.contrib.admin.widgets import FilteredSelectMultiple
from mptt.forms import TreeNodeChoiceField
from main.models import UIDStatus, Role, ErrorType, UIDError, Project

class ErrorForm(forms.ModelForm):
    '''
    This is an error form which is to be filled in for associating errors
    with a UID.
    Call it via ajax for error.

    '''
    etype = TreeNodeChoiceField(label=_('Select Error Type'), initial=0, queryset=ErrorType.objects.all(),
            widget=forms.HiddenInput(attrs={'class':'error_types'}))

    class Meta:
        model = UIDError
        exclude = ('uid_status', )

    def __init__(self, role,uid_status=None, *args, **kwargs):
        super(ErrorForm, self).__init__(*args, **kwargs)
        self.uid_status = uid_status
        project = role.get_project()
        query = Q()
        # This generates a query which filters trees from error type
        # according to the project's linked error types
        for et in project.error_types.all():
            q = Q(lft__gte=et.lft, rght__lte=et.rght)
            query |= q
        self.fields['etype'].queryset = ErrorType.objects.filter(query).order_by('level')

    def clean_etype(self):
        #et = ErrorType.objects.get(pk=int(self.cleaned_data['etype']))
        et = self.cleaned_data['etype']
        if et.is_leaf_node():
            return self.cleaned_data['etype']
        else:
            raise forms.ValidationError("A leaf node is required.")
    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(ErrorForm, self).save(commit=False)
        m.uid_status = self.uid_status
        if commit:
            m.save()
        return m

class UIDForm(forms.Form):
    uid = forms.CharField(label="UID", required=True)

    def __init__(self, role, date, *args, **kwargs):
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
                                                    _('select UIDs'),
                                                    True,
                                                 ))

    def __init__(self, role, *args, **kwargs):
        super(UIDAssignmentForm, self).__init__(*args, **kwargs)
        self.fields['uids'].queryset = role.managed_uids()

class ProjectAdminForm(forms.ModelForm):
    hierarchy = forms.ModelChoiceField(queryset=Role.objects.filter(head__isnull=True))
    error_types = forms.ModelMultipleChoiceField(queryset=ErrorType.objects.filter(parent__isnull=True))

    class Meta:
        model=Project

    def __init__(self, *args, **kwargs):
        super(ProjectAdminForm, self).__init__(*args, **kwargs)
