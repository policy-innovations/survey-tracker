from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from django.core import serializers
import settings
from main.forms import EntryForm
from main.models import *

def home(request):
    return render(request, 'main/home.html',)

def new_entry(request):
    form = EntryForm()
    return render(request, 'main/new_entry.html', {'form':form})

def get_error_types(request):
    mimetype = 'application/json'
    json_serializer = serializers.get_serializer("json")()
    data = json_serializer.serialize(ErrorType.objects.all(),
            ensure_ascii=False, fields=('name', 'id', 'parent', 'level'))
    return HttpResponse(data, mimetype)
