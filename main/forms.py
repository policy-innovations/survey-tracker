from django import forms
from main.models import *

class EntryForm(forms.ModelForm):
    errors = forms.ModelChoiceField(ErrorType.objects.all().filter(level=0), 
            empty_label="Select one error" )

    class Meta:
        model = UIDStatus
