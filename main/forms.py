from django import forms
from main.models import *

class UIDStatusForm(forms.ModelForm):
    class Meta:
        model = UIDStatus

class UIDErrorForm(forms.ModelForm):
    choices = [('','-----------'),]
    for e in ErrorType.objects.all().filter(level=0):
        choices.append((e.pk, e.name))
    etype = forms.ChoiceField(label="Errors", widget=forms.Select(attrs={
        'class':'error_types'}), choices=choices)
    class Meta:
        model = UIDError
