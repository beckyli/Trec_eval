from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse

from trec.forms import UserForm, UserUpdateForm, ResearcherForm
from trec.models import Researcher

def index(request):
    return HttpResponse("This is the index")

def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        researcher_form = ResearcherForm(data=request.POST)
        if user_form.is_valid() and researcher_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            researcher = researcher_form.save(commit=False)
            researcher.user = user
            if 'profile_pic' in request.FILES:
                researcher.profile_pic = request.FILES['profile_pic']
            researcher.save()
            return redirect('/')
        else:
            print user_form.errors, researcher_form.errors
    else:
        user_form = UserForm()
        researcher_form = ResearcherForm()
    return render(request, 'trec/register.html',
                  {'user_form': user_form, 'researcher_form': researcher_form})

@login_required
def profile(request):
    user = request.user
    researcher = Researcher.objects.get(user=user)
    if request.method == 'POST':
        user_form = UserUpdateForm(data=request.POST, instance=user)
        researcher_form = ResearcherForm(data=request.POST, instance=researcher)
        if user_form.is_valid() and researcher_form.is_valid():
            user.save()
            if 'profile_pic' in request.FILES:
                researcher.profile_pic = request.FILES['profile_pic']
            researcher.save()
            return redirect('/')
        else:
            print user_form.errors, researcher_form.errors
    else:
        user_form = UserUpdateForm(instance=user)
        researcher_form = ResearcherForm(instance=researcher)
    return render(request, 'trec/profile.html',
                  {'user_form': user_form, 'researcher_form': researcher_form})
