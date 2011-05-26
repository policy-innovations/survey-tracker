from django import forms
from main.models import *

class UIDStatusForm(forms.ModelForm):
    class Meta:
        model = UIDStatus

class UIDErrorForm(forms.ModelForm):
    etype = forms.ModelChoiceField(ErrorType.objects.all().filter(level=0),
                        empty_label="----------" )
    class Meta:
        model = UIDError
