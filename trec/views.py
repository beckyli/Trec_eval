from django.shortcuts import render
from django.http import HttpResponse
import os
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.

def index(request):

    return HttpResponse("This is the index")
