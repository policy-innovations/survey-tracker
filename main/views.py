from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from django.utils.functional import curry
from django.utils import simplejson
from main.forms import ErrorForm, UIDForm
from main.models import ErrorType, Role

def home(request):
    return render(request, 'main/home.html',)

@login_required
def add_entry(request, proj_pk):
    role = get_object_or_404(Role, user=request.user)
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

def get_error_types(request):
    mimetype = 'application/json'
    json_serializer = serializers.get_serializer("json")()
    data = json_serializer.serialize(ErrorType.objects.all(),
            ensure_ascii=False, fields=('name', 'id', 'parent', 'level'))
    return HttpResponse(data, mimetype)

def get_errors(request):
    mimetype = 'application/json'
    #json_serializer = serializers.get_serializer("json")()
    errors = []
    for e in ErrorType.objects.all().filter(level=0):
        d = {}
        children = []
        for ec in e.get_children():
            c = {}
            c['pk'] = ec.pk
            c['name'] = ec.name
            children.append(c)
        d['pk'] = e.pk
        d['name'] = e.name
        d['children'] = children
        errors.append(d)
    print errors
    #data = json_serializer.serialize(errors, ensure_ascii=False)
    #return HttpResponse(data, mimetype)
    return HttpResponse(simplejson.dumps(errors), mimetype)
