# Create your views here.
from django.http import Http404,HttpResponseRedirect
from django.shortcuts import render_to_response
from couchdb.client import ResourceNotFound

def home(request):
    pass
