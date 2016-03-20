from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse

from trec.forms import *
from trec.models import Researcher, Task, Track
from trec.utils import run_trec_eval


def index(request):
    track_list = Track.objects.order_by('-title')
    context_dict = {'tracks': track_list}
    return render(request, 'trec/index.html', context_dict)

def about(request):
    return render(request, 'trec/about.html')

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

            user = authenticate(username=user.username,
                                password=user_form.cleaned_data['password'])
            login(request, user)
            return redirect(index)
    else:
        user_form = UserForm()
        researcher_form = ResearcherForm()
    return render(request, 'trec/register.html',
                  {'user_form': user_form, 'researcher_form': researcher_form})

def user_login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(index)
            context['error'] = 'Your TREC Evaluator account is disabled.'
        else:
            context['error'] = 'Invalid login details supplied.'
    return render(request, 'trec/login.html', context)

def user_logout(request):
    logout(request)
    return redirect(index)

def tracks(request):
    tracks = Track.objects.all()
    for track in tracks:
        track.tasks = Task.objects.filter(track=track)
    return render(request, 'trec/tracks.html', {'tracks': tracks})

def track(request, track_slug):
    try:
        track = Track.objects.get(slug=track_slug)
    except Track.DoesNotExist:
        return redirect(index)

    tasks = Task.objects.filter(track=track)

    return render(request, 'trec/track.html',{'tasks': tasks, 'track': track})

def task_results(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return redirect(index)

    runs = Run.objects.filter(task=task)                

    return render(request, 'trec/view_task_runs.html',
                  {'runs': runs, 'task': task})

def researchers(request):
    researchers = Researcher.objects.all()
    return render(request, 'trec/researchers.html',
                  {'researchers': researchers})

def researcher(request, username):
    try:
        user = User.objects.get(username=username)
        researcher = Researcher.objects.get(user=user)
    except (User.DoesNotExist, Researcher.DoesNotExist):
        return redirect(index)
    runs = Run.objects.filter(researcher=researcher)
    return render(request, 'trec/researcher.html', {"runs": runs,
                                                    'researcher': researcher})

@login_required
def add_track(request):
    user = request.user

    if not user.is_superuser:
        return render(request, 'trec/add_track.html', {})
    else:
        if request.method == 'POST':
            track_form = TrackForm(request.POST)
            if track_form.is_valid():
                track_form.save(commit=True)
                return redirect(index)
        else:
            track_form = TrackForm(instance=user)
        return render(request, 'trec/add_track.html', {'track_form': track_form})

@login_required
def profile(request):
    user = request.user
    researcher = Researcher.objects.get(user=user)
    runs = Run.objects.filter(researcher=researcher)
    return render(request, 'trec/researcher.html', {'researcher': researcher,
                                                    'runs': runs})

@login_required
def edit_profile(request):
    user = request.user
    researcher = Researcher.objects.get(user=user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        researcher_form = ResearcherForm(request.POST, instance=researcher)
        if user_form.is_valid() and researcher_form.is_valid():
            user.save()
            if 'profile_pic' in request.FILES:
                researcher.profile_pic = request.FILES['profile_pic']
            researcher.save()
            return redirect(index)
    else:
        user_form = UserUpdateForm(instance=user)
        researcher_form = ResearcherForm(instance=researcher)
    return render(request, 'trec/edit_profile.html',
                  {'user_form': user_form, 'researcher_form': researcher_form})

@login_required
def submit_run(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return redirect(index)
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
                return render(request, 'trec/run.html', {'run': run})
            form.add_error('results_file',
                           'There was a problem evaluating your results file')
            run.delete()
    else:
        form = RunForm()
    return render(request, 'trec/submit_run.html', {'form': form, 'task': task})
