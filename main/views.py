from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from django.utils.functional import curry
from django.utils import simplejson
from django.core.urlresolvers import reverse
from main.forms import ErrorForm, UIDForm
from main.models import ErrorType, Role, Project, UIDStatus

def home(request):
    return render(request, 'main/home.html',)

@login_required
def select_surveyor(request, proj_pk):
    project = Project.objects.get(pk=proj_pk)
    role = project.hierarchy.get_descendants(include_self=True).get(
            user=request.user)
    surveyors = role.get_leafnodes()
    return render(request, 'main/select_surveyor.html',
            {'surveyors':surveyors})

@login_required
def add_completed_entry(request, role_id):
    role = Role.objects.get(id=role_id)
    UIDFormset = formset_factory(UIDForm)
    UIDFormset.form = staticmethod(curry(UIDForm, role))
    if request.method == 'POST':
        formset = UIDFormset(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                form.save()
            return HttpResponseRedirect(reverse('add-completed-entry-done',
                kwargs={'role_id':role.id,}))
        else:
            return render(request, 'main/add_completed_entry.html',
                    {'formset':formset})
    else:
        formset = UIDFormset()
        return render(request, 'main/add_completed_entry.html',
                {'formset':formset})

@login_required
def add_completed_entry_done(request, role_id):
    role = Role.objects.get(id=role_id)
    return render(request, 'main/add_completed_entry_done.html', {'role':role})


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
