from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from django.core import serializers
from django.forms.formsets import formset_factory
import settings
from main.forms import *
from main.models import *

def home(request):
    return render(request, 'main/home.html',)

def new_entry(request):
    count = len(ErrorType.objects.all().filter(level=0))
    uid_status_form = UIDStatusForm()
    uid_error_formset = formset_factory(UIDErrorForm, extra=count)
    return render(request, 'main/new_entry.html', {'uid_status_form':
        uid_status_form, 'uid_error_formset':uid_error_formset})

def get_error_types(request):
    mimetype = 'application/json'
    json_serializer = serializers.get_serializer("json")()
    data = json_serializer.serialize(ErrorType.objects.all(),
            ensure_ascii=False, fields=('name', 'id', 'parent', 'level'))
    return HttpResponse(data, mimetype)
