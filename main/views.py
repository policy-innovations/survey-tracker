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
from main.models import ErrorType, Role, Questionnaire, UIDStatus

def home(request):
    return render(request, 'main/home.html',)

@login_required
def select_surveyor(request, proj_pk):
    questionnaire = Questionnaire.objects.get(pk=proj_pk)
    role = questionnaire.hierarchy.get_descendants(include_self=True).get(
            user=request.user)
    surveyors = role.get_leafnodes()
    return render(request, 'main/select_surveyor.html',
            {'surveyors':surveyors})

@login_required
def add_completed_entry(request, role_id):
    role = Role.objects.get(id=role_id)
    questionnaire = role.get_questionnaire()
    QuestionFormset = formset_factory(QuestionForm,
            extra=len(questionnaire.questions.all()),
            max_num = len(QuestionType.objects.all().filter(level=0)))
    QuestionFormset.form = staticmethod(curry(QuestionForm, role))
    if request.method == 'POST':
        d = request.POST.get('date').split('-')
        date = _date(year=int(d[0]), month=int(d[1]), day=int(d[2]))
        uid_form = UIDForm(role, date, request.POST, request.FILES)
        question_formset = QuestionFormset()

        if uid_form.is_valid():
            uid_status = uid_form.save()
        else:
            return render(request, 'main/add_completed_entry.html',
                    {'uid_form':uid_form, 'question_formset':question_formset,
                        'date':date, 'role':role})

        QuestionFormset.form = staticmethod(curry(QuestionForm, role, uid_status))
        question_formset = QuestionFormset(request.POST, request.FILES)
        if question_formset.is_valid():
            for form in question_formset:
                form.save()
            return HttpResponseRedirect(reverse('add-completed-entry-done',
                kwargs={'role_id':role.id}))
        else:
            return render(request, 'main/add_completed_entry.html',
                    {'uid_form':uid_form, 'question_formset':question_formset,
                        'date':date, 'role':role})
    else:
        date = _date.today() - _timedelta(days=2)
        uid_form = UIDForm(role, date)
        question_formset = QuestionFormset()
        return render(request, 'main/add_completed_entry.html',
                {'uid_form':uid_form, 'question_formset':question_formset,
                    'date':date, 'role':role})

@login_required
def add_completed_entry_done(request, role_id):
    role = Role.objects.get(id=role_id)
    return render(request, 'main/add_completed_entry_done.html', {'role':role})

@login_required
def add_uncompleted_entry(request, role_id):
    role = Role.objects.get(id=role_id)
    ErrorFormset = formset_factory(ErrorForm, extra=1,
            max_num = len(ErrorType.objects.all().filter(level=0)))
    ErrorFormset.form = staticmethod(curry(ErrorForm, role))
    if request.method == 'POST':
        d = request.POST.get('date').split('-')
        date = _date(year=int(d[0]), month=int(d[1]), day=int(d[2]))
        uid_form = UIDForm(role, date, request.POST, request.FILES)
        error_formset = ErrorFormset()

        if uid_form.is_valid():
            uid_status = uid_form.save()
        else:
            return render(request, 'main/add_uncompleted_entry.html',
                    {'uid_form':uid_form, 'error_formset':error_formset,
                        'date':date, 'role':role})

        ErrorFormset.form = staticmethod(curry(ErrorForm, role, uid_status))
        error_formset = ErrorFormset(request.POST, request.FILES)
        if error_formset.is_valid():
            for form in error_formset:
                form.save()
            return HttpResponseRedirect(reverse('add-uncompleted-entry-done',
                kwargs={'role_id':role.id}))
        else:
            return render(request, 'main/add_uncompleted_entry.html',
                    {'uid_form':uid_form, 'error_formset':error_formset,
                        'date':date, 'role':role})
    else:
        date = _date.today() - _timedelta(days=2)
        uid_form = UIDForm(role, date)
        error_formset = ErrorFormset()
        return render(request, 'main/add_uncompleted_entry.html',
                {'uid_form':uid_form, 'error_formset':error_formset,
                    'date':date, 'role':role})

@login_required
def add_uncompleted_entry_done(request, role_id):
    role = Role.objects.get(id=role_id)
    return render(request, 'main/add_uncompleted_entry_done.html', {'role':role})

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
