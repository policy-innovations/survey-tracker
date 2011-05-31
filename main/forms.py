from django import forms
from django.db.models import Q, F

from mptt.forms import TreeNodeChoiceField
from main.models import *

class UIDStatusForm(forms.ModelForm):
    class Meta:
        model = UIDStatus
        exclude = ('errors', 'role', 'project')

class UIDErrorForm(forms.ModelForm):
    choices = [('','-----------'),]
    for e in ErrorType.objects.all().filter(level=0):
        choices.append((str(e.pk), e.name))
    etype = forms.ChoiceField(label="Errors", widget=forms.Select(attrs={
        'class':'error_types'}), choices=choices)
    class Meta:
        model = UIDError
        exclude = ('uid_status',)

class ErrorForm(forms.ModelForm):
    '''
    This is an error form which is to be filled in for associating errors
    with a UID.
    Call it via ajax for error.

    '''
    etype = TreeNodeChoiceField(queryset=ErrorType.objects.all(),
            widget=forms.Select(attrs={'class':'error_types'}))

    class Meta:
        model = UIDError

    def __init__(self, role, *args, **kwargs):
        super(ErrorForm, self).__init__(*args, **kwargs)
        self.fields['uid_status'].queryset = role.uids()
        project = role.get_project()
        query = Q()
        # This generates a query which filters trees from error type
        # according to the project's linked error types
        for et in project.error_types.all():
            q = Q(lft__gte=et.lft, rght__lte=et.rght)
            query |= q
        self.fields['etype'].queryset = ErrorType.objects.filter(query).order_by('level')
        #self.fields['etype'].queryset = err_type.get_descendants(include_self=True)

    def clean_etype(self):
        et = self.cleaned_data['etype']
        if et.is_leaf_node():
            return self.cleaned_data['etype']
        else:
            raise forms.ValidationError("A leaf node is required.")

# This is yet to be completed
class UIDForm(forms.Form):
    completer = forms.ModelChoiceField(queryset=Role.objects.all())
    #error_types = forms.ModelChoiceField(queryset=ErrorType.objects.all())


class ProjectAdminForm(forms.ModelForm):
    hierarchy = forms.ModelChoiceField(queryset=Role.objects.filter(head__isnull=True))
    error_types = forms.ModelMultipleChoiceField(queryset=ErrorType.objects.filter(parent__isnull=True))

    class Meta:
        model=Project

    def __init__(self, *args, **kwargs):
        form = super(ProjectAdminForm, self).__init__(*args, **kwargs)
