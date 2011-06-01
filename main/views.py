from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from django.utils.functional import curry
from django.utils import simplejson
from main.forms import ErrorForm, UIDForm
from main.models import ErrorType, Role, Project

def home(request):
    return render(request, 'main/home.html',)

@login_required
def select_surveyor(request, proj_pk):
    project = Project.objects.get(pk=proj_pk)
    surveyors = project.hierarchy.get_leafnodes()
    return render(request, 'main/select_surveyor.html',
            {'surveyors':surveyors})

@login_required
def add_entry(request, role_id):
    role = Role.objects.get(id=role_id)
    ErrorFormset = formset_factory(ErrorForm, extra = len(ErrorType.objects.all().filter(level=0)))
    ErrorFormset.form = staticmethod(curry(ErrorForm, role))
    if request.method == 'POST':
        formset = ErrorFormset(request.POST, request.FILES)
        #print formset
        if formset.is_valid():
            for form in formset:
                print form
    else:
        formset = ErrorFormset()
        uid_form = UIDForm()
        return render(request, 'main/add_entry.html', {'uid_form':uid_form,
            'formset':formset})

@login_required
def manage_uids(request, role_id):
    role = Role.objects.get(id=role_id)
    context = {
        'role':role,
    }
    return render(request, 'main/manage_uids.html', context)

@login_required
def manage_sub_uids(request, role_id, sub_role):
    role = Role.objects.get(id=role_id)

    context = {
        'role':role,
    }
    return render(request, 'main/manage_sub_uids.html', context)

def get_error_types(request):
    mimetype = 'application/json'
    json_serializer = serializers.get_serializer("json")()
    data = json_serializer.serialize(ErrorType.objects.all(),
            ensure_ascii=False, fields=('name', 'id', 'parent', 'level'))
    return HttpResponse(data, mimetype)
