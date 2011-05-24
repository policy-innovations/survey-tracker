from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
import settings

def home(request):
    return render(request, 'main/home.html',)
