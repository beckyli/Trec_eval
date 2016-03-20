from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse

from trec.forms import *
from trec.models import Researcher, Task, Track
from trec.utils import run_trec_eval
import json
from chartit import DataPool, Chart

def index(request):
    track_list = Track.objects.order_by('-title')
    context_dict = {'tracks': track_list}
    return render(request, 'trec/index.html', context_dict)

def about(request):
    return render(request, 'trec/about.html')

def ajax_results_query_responder(request):

    if request.method == 'GET':

        print request.GET['data']
        data = json.loads(request.GET['data'])
        print data
        researchers = data['researchers']
        tasks = data['tasks']
        order_by = data['order_by']
        direction = data['direction']
        headers = data['headers']
        results_for = data['results_for']
        researcher_or_task = data['researcher_or_task']

        if researchers != None:
            try:
                users = User.objects.filter(username__in=researchers)
                researchers = Researcher.objects.filter(user=users)
            except User.DoesNotExist, Researcher.DoesNotExist:
                return HttpResponse('Error finding user', status=500)

        if tasks != None:
            try:
                tasks = Task.objects.filter(pk__in=tasks)
            except Task.DoesNotExist:
                return HttpResponse('Error finding task', status=500)

        if direction == 'ascending':
            try:
                runs = Run.objects.filter(researcher=researchers, task=tasks).order_by('-'+order_by)
                direction = 'descending'
            except Run.DoesNotExist:
                return HttpResponse('Error finding Run', status=500)
        else:
            try:
                runs = Run.objects.filter(researcher=researchers, task=tasks).order_by(order_by)
                direction = 'ascending'
            except Run.DoesNotExist:
                return HttpResponse('Error finding Run', status=500)

        if researcher_or_task == 'researcher':
            return render(request, 'trec/table.html', {'rows': runs, 'headers': headers, 'direction': direction,
                                                       'results_for': results_for, "researcher": True })
        elif researcher_or_task == 'task':
            return render(request, 'trec/table.html', {'rows': runs, 'headers': headers, 'direction': direction,
                                                       'results_for': results_for, "task": True })


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
    #
    # precision_data = \
    #     DataPool (
    #         series =
    #             [{'options': {
    #                 'source': Run.objects.all()},
    #               'terms': [
    #                   'researcher',
    #                   'map',
    #                   'p10',
    #                   'p20',]}
    #              ])
    # cht = Chart(
    #         data_source = precision_data,
    #         series_options = [
    #              {'options':{
    #                 'type': 'column',
    #                 'stacking': False,
    #                 'stack': 0},
    #               'terms':{ [
    #                   'map']}},
    #
    #              {'options':{
    #                 'type': 'column',
    #                 'stacking': False,
    #                 'stack': 1},
    #               'terms':{ [
    #                   'p10']}},
    #
    #              {'options':{
    #                 'type': 'column',
    #                 'stacking': False,
    #                 'stack': 2},
    #               'terms':{ [
    #                   'p20']}
    #               }],
    #         chart_options =
    #             {'title': {
    #                 'text': 'Results'},
    #              'xAxis': {
    #                  'title': {
    #                      'text': 'Researcher'}}})
    #
                      

    return render(request, 'trec/view_task_runs.html',
                  {'runs': runs, 'task': task})
                   #'precision_chart': cht})

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
