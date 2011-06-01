from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.core import serializers
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from django.utils.functional import curry
from django.utils import simplejson
from django.core.urlresolvers import reverse
from datetime import date as _date
from datetime import timedelta as _timedelta
from main.forms import ErrorForm, UIDForm, UIDAssignmentForm
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
    if request.method == 'POST':
        print request.POST
        d = request.POST.get('date').split('-')
        date = _date(year=int(d[0]), month=int(d[1]), day=int(d[2]))
        UIDFormset.form = staticmethod(curry(UIDForm, role, date))
        formset = UIDFormset(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                form.save()
            return HttpResponseRedirect(reverse('add-completed-entry-done',
                kwargs={'role_id':role.id}))
        else:
            return render(request, 'main/add_completed_entry.html',
                    {'formset':formset, 'date':date})
    else:
        date = _date.today() - _timedelta(days=2)
        UIDFormset.form = staticmethod(curry(UIDForm, role, date))
        formset = UIDFormset()
        return render(request, 'main/add_completed_entry.html',
                {'formset':formset, 'date':date})

@login_required
def add_completed_entry_done(request, role_id):
    role = Role.objects.get(id=role_id)
    return render(request, 'main/add_completed_entry_done.html', {'role':role})


@login_required
def manage_uids(request, role_id):
    role = Role.objects.get(id=role_id)
    if not request.user == role.user:
        raise Http404

    manages = role.managed_uids().count() > 0

    context = {
        'role':role,
        'manages':manages,
    }
    return render(request, 'main/manage_uids.html', context)

@login_required
def manage_sub_uids(request, role_id, sub_role):
    role = Role.objects.get(id=role_id)
    if not request.user == role.user:
        raise Http404

    subordinate = role.get_children().get(id=sub_role)
    manages = role.managed_uids().count() > 0

    if request.method=='POST':
        form = UIDAssignmentForm(role, request.POST)
        if form.is_valid():
            return redirect(reverse('manage-sub-uids', kwargs={
                    'role_id':role_id,
                    'sub_role':sub_role,
                }))
    else:
        form = UIDAssignmentForm(role,
                                 initial={
                                    'uids':subordinate.uidstatuses.all(),
                                 })

    context = {
        'role':role,
        'sub':subordinate,
        'form':form,
        'manages':manages,
    }
    return render(request, 'main/manage_sub_uids.html', context)

def get_error_types(request):
    mimetype = 'application/json'
    json_serializer = serializers.get_serializer("json")()
    data = json_serializer.serialize(ErrorType.objects.all(),
            ensure_ascii=False, fields=('name', 'id', 'parent', 'level'))
    return HttpResponse(data, mimetype)
