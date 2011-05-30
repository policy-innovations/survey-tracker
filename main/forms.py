from django import forms
from main.models import *

class UIDStatusForm(forms.ModelForm):
    class Meta:
        model = UIDStatus
        exclude = ('errors', 'role', 'project')

class UIDErrorForm(forms.ModelForm):
    choices = [('','-----------'),]
    for e in ErrorType.objects.all().filter(level=0):
        choices.append((str(e.pk), e.name))
    print len(choices)
    etype = forms.ChoiceField(label="Errors", widget=forms.Select(attrs={
        'class':'error_types'}), choices=choices)
    class Meta:
        model = UIDError
        exclude = ('uid_status',)

class ProjectAdminForm(forms.ModelForm):
    hierarchy = forms.ModelChoiceField(queryset=Role.objects.filter(head__isnull=True))
    error_types = forms.ModelMultipleChoiceField(queryset=ErrorType.objects.filter(parent__isnull=True))

    class Meta:
        model=Project

    def __init__(self, *args, **kwargs):
        form = super(ProjectAdminForm, self).__init__(*args, **kwargs)
