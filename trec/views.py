from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse

from trec.forms import *
from trec.models import Researcher, Task
from trec.utils import run_trec_eval

def index(request):
    return HttpResponse("This is the index")

def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        researcher_form = ResearcherForm(request.POST)
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
        user_form = UserUpdateForm(equest.POST, instance=user)
        researcher_form = ResearcherForm(request.POST, instance=researcher)
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

@login_required
def submit_run(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return redirect('/')
    if request.method == 'POST':
        form = RunForm(request.POST, request.FILES)
        if form.is_valid():
            run = form.save(commit=False)
            run.researcher = Researcher.objects.get(user=request.user)
            run.task = task
            run.save() # needed to upload the file to its place
            run.map, run.p10, run.p20 = run_trec_eval(task.judgement_file.path,
                                                      run.results_file.path)
            if run.map is not None:
                run.save()
                return redirect('/')
            form._errors['results_file'] = form.error_class(
                [u'There was a problem evaluating your results file'])
            run.delete()
        else:
            print form.errors
    else:
        form = RunForm()
    return render(request, 'trec/submit_run.html', {'form': form, 'task': task})
