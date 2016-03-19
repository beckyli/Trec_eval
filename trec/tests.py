import os

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase

from populate_trec import add_researcher, add_task, add_track
from trec_project.settings import MEDIA_ROOT

class IndexViewTests(TestCase):

    def test_get_request(self):
        'Should render trec/index.html with a tracks object.'
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed('trec/index.html')
        self.assertIn('tracks', response.context)

class AboutViewTests(TestCase):

    def test_get_request(self):
        'Should render trec/about.html template.'
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed('trec/about.html')

class RegisterViewTests(TestCase):

    def test_get_request(self):
        'Both forms should be displayed.'
        response = self.client.get(reverse('register'))
        self.assertIn('user_form', response.context)
        self.assertIn('researcher_form', response.context)

    def test__post_request(self):
        'Should redirect to the index page.'
        data = {'username': 'jill', 'password': 'jill',
                'profile_pic': SimpleUploadedFile('file.jpg', 'file_content'),
                'website': 'http://google.com/',
                'display_name': 'Jill', 'organisation': 'Jillian'}
        response = self.client.post(reverse('register'), data)
        self.assertRedirects(response, '/')

class UserLoginViewTests(TestCase):

    def setUp(self):
        user = User(username='jill')
        user.set_password('jill')
        user.save()

    def test_bad_input(self):
        'Returned page should have an appropriate error message.'
        response = self.client.post(reverse('login'), {})
        self.assertContains(response, 'Invalid login details supplied.')

    def test_active_user(self):
        'Should redirect to the index page.'
        response = self.client.post(reverse('login'), {'username': 'jill',
                                                       'password': 'jill'})
        self.assertRedirects(response, '/')

    def test_inactive_user(self):
        'Returned page should have an appropriate error message.'
        user = User.objects.get(username='jill')
        user.is_active = False
        user.save()
        response = self.client.post(reverse('login'), {'username': 'jill',
                                                       'password': 'jill'})
        self.assertContains(response,
                            'Your TREC Evaluator account is disabled.')

class UserLogoutViewTests(TestCase):

    def test_get_request(self):
        'Should redirect to the index page.'
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, '/')

class TracksViewTests(TestCase):

    def test_get_request(self):
        'Ouput should contain tracks object.'
        add_track('track')
        response = self.client.get(reverse('tracks'))
        self.assertIn('tracks', response.context)

class TrackViewTests(TestCase):

    def test_bad_track(self):
        'Should redirect to the index page.'
        response = self.client.get('/track/nonexistant/')
        self.assertRedirects(response, '/')

    def test_good_track(self):
        'Ouput should contain tasks and track objects.'
        track = add_track('track')
        response = self.client.get('/track/{}/'.format(track.slug))
        self.assertIn('tasks', response.context)
        self.assertIn('track', response.context)

class TaskResultsViewTests(TestCase):

    def test_bad_task(self):
        'Should redirect to the index page.'
        response = self.client.get('/task/666/')
        self.assertRedirects(response, '/')

    def test_good_task(self):
        'Should render runs and task objects.'
        track = add_track('track')
        add_task(track, 'task', os.path.join(MEDIA_ROOT, 'judgement_files',
                                             'dg.trec.qrels'))
        response = self.client.get('/task/1/')
        self.assertIn('runs', response.context)
        self.assertIn('task', response.context)

class ResearchersViewTests(TestCase):

    def test_get_request(self):
        'Output should contain the researchers object.'
        response = self.client.get(reverse('researchers'))
        self.assertIn('researchers', response.context)

class ResearcherViewTests(TestCase):

    def test_bad_username(self):
        'Should redirect to the index page.'
        response = self.client.get('/researcher/nonexistant/')
        self.assertRedirects(response, '/')

    def test_good_username(self):
        'Output should contain runs and researcher objects.'
        add_researcher('jill')
        response = self.client.get('/researcher/jill/')
        self.assertIn('runs', response.context)
        self.assertIn('researcher', response.context)

class AddTrackViewTests(TestCase):

    def setUp(self):
        add_researcher('jill')
        self.client.login(username='jill', password='jill')

    def set_up(self):
        user = User.objects.get(username='jill')
        user.is_superuser = True
        user.save()

    def test_with_a_regular_user(self):
        'Should render the add_track.html template without the track_form.'
        response = self.client.get(reverse('add_track'))
        self.assertTemplateUsed('trec/add_track.html')
        self.assertNotContains(response, 'track_form')

    def test_get_request(self):
        'Output should the track_form.'
        self.set_up()
        response = self.client.get(reverse('add_track'))
        self.assertIn('track_form', response.context)

    def test_valid_post_request(self):
        'Should redirect to the index page.'
        self.set_up()
        response = self.client.post(reverse('add_track'),
                                    {'title': 'title',
                                     'track_url': 'http://google.com/',
                                     'description': 'description',
                                     'genre': 'genre'})
        self.assertRedirects(response, '/')

class ProfileViewTests(TestCase):

    def test_get_request(self):
        'Should contain researcher and runs objects.'
        add_researcher('jill')
        self.client.login(username='jill', password='jill')
        response = self.client.get(reverse('profile'))
        self.assertIn('researcher', response.context)
        self.assertIn('runs', response.context)

class EditProfileViewTests(TestCase):

    def setUp(self):
        add_researcher('jill')
        self.client.login(username='jill', password='jill')

    def test_get_request(self):
        'Both forms should be displayed.'
        response = self.client.get(reverse('edit_profile'))
        self.assertIn('user_form', response.context)
        self.assertIn('researcher_form', response.context)

    def test_successful_post_request(self):
        'Should redirect to the index page.'
        data = {'username': 'jill',
                'profile_pic': SimpleUploadedFile('file.jpg', 'file_content'),
                'website': 'http://google.com/', 'display_name': 'Jill',
                'organisation': 'Jillian'}
        response = self.client.post(reverse('edit_profile'), data)
        self.assertRedirects(response, '/')

class SubmitRunViewTest(TestCase):

    def setUp(self):
        track = add_track('track')
        add_task(track, 'task',
                 judge=os.path.join(MEDIA_ROOT, 'judgement_files',
                                    'ap.trec.qrels'))
        add_researcher('jill')
        self.client.login(username='jill', password='jill')

    def test_with_bad_task(self):
        'Should redirect to the index page.'
        response = self.client.get('/task/666/submit/')
        self.assertRedirects(response, '/')

    def test_get_request(self):
        'Should render the form.'
        response = self.client.get('/task/1/submit/')
        self.assertIn('form', response.context)

    def test_bad_file(self):
        'Should display an error message.'
        data = {'name': 'run', 'description': 'Run',
                'results_file': SimpleUploadedFile('file.res', 'file_content'),
                'run_type': 'a', 'query_type': 'title', 'feedback_type': 'none'}
        response = self.client.post('/task/1/submit/', data)
        self.assertContains(response,
                            'There was a problem evaluating your results file')

    def test_good_file(self):
        'Should render trec/run.html template with a run object.'
        data = {'name': 'run', 'description': 'Run',
                'results_file': open(os.path.join(MEDIA_ROOT, 'results',
                                                  'ap.trec.bm25.0.50.res')),
                'run_type': 'a', 'query_type': 'title', 'feedback_type': 'none'}
        response = self.client.post('/task/1/submit/', data)
        self.assertTemplateUsed('trec/run.html')
        self.assertIn('run', response.context)
