import os

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase

from populate_trec import add_researcher, add_task, add_track
from trec_project.settings import MEDIA_ROOT

class RegisterViewTests(TestCase):

    def test_get_request(self):
        'Both forms should be displayed.'
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('user_form', response.context)
        self.assertIn('researcher_form', response.context)

    def test_successful_post_request(self):
        'Should redirect to the index page.'
        data = {'username': 'jill', 'password': 'jill',
                'profile_pic': SimpleUploadedFile('file.jpg', 'file_content'),
                'website': 'http://google.com/',
                'display_name': 'Jill', 'organisation': 'Jillian'}
        response = self.client.post(reverse('register'), data)
        self.assertRedirects(response, '/')

    def test_unsuccessful_post_request(self):
        'Should render the forms again.'
        response = self.client.post(reverse('register'), {})
        self.assertEqual(response.status_code, 200)
        self.assertIn('user_form', response.context)
        self.assertIn('researcher_form', response.context)

class LoginViewTests(TestCase):

    def test_get_request(self):
        'Should render trec/login.html.'
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('trec/login.html')

    def test_bad_input(self):
        'Returned page should have an appropriate error message.'
        response = self.client.post(reverse('login'), {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid login details supplied.')

    def test_active_user(self):
        'Should redirect to the index page.'
        user = User(username='jill')
        user.set_password('jill')
        user.save()
        response = self.client.post(reverse('login'), {'username': 'jill',
                                                       'password': 'jill'})
        self.assertRedirects(response, '/')

    def test_inactive_user(self):
        'Returned page should have an appropriate error message.'
        user = User(username='jill')
        user.set_password('jill')
        user.is_active = False
        user.save()
        response = self.client.post(reverse('login'), {'username': 'jill',
                                                       'password': 'jill'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            'Your TREC Evaluator account is disabled.')

class LogoutViewTests(TestCase):

    def test_get_request(self):
        'Should redirect to the index page.'
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, '/')

class ProfileViewTests(TestCase):

    def test_with_no_user(self):
        'Should redirect to the login page.'
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, 'login/?next=/profile/')

    def set_up(self):
        add_researcher('jill')
        self.client.login(username='jill', password='jill')

    def test_get_request(self):
        'Both forms should be displayed.'
        self.set_up()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('user_form', response.context)
        self.assertIn('researcher_form', response.context)

    def test_successful_post_request(self):
        'Should redirect to the index page.'
        self.set_up()
        data = {'username': 'jill',
                'profile_pic': SimpleUploadedFile('file.jpg', 'file_content'),
                'website': 'http://google.com/', 'display_name': 'Jill',
                'organisation': 'Jillian'}
        response = self.client.post(reverse('profile'), data)
        self.assertRedirects(response, '/')

    def test_unsuccessful_post_request(self):
        'Should render the forms again.'
        self.set_up()
        response = self.client.post(reverse('profile'), {})
        self.assertEqual(response.status_code, 200)
        self.assertIn('user_form', response.context)
        self.assertIn('researcher_form', response.context)

class SubmitRunViewTest(TestCase):

    def setUp(self):
        track = add_track('track')
        add_task(track, 'task',
                 judge=os.path.join(MEDIA_ROOT, 'judgement_files',
                                    'ap.trec.qrels'))

    def set_up_user(self):
        add_researcher('jill')
        self.client.login(username='jill', password='jill')

    def test_with_no_user(self):
        'Should redirect to the login page.'
        response = self.client.get('/task/1/submit/')
        self.assertRedirects(response, 'login/?next=/task/1/submit/')

    def test_with_no_task(self):
        'Should redirect to the index page.'
        self.set_up_user()
        response = self.client.get('/task/2/submit/')
        self.assertRedirects(response, '/')

    def test_get_request(self):
        'Should render the form.'
        self.set_up_user()
        response = self.client.get('/task/1/submit/')
        self.assertEquals(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_bad_file(self):
        'Should display an error message.'
        self.set_up_user()
        data = {'name': 'run',
                'results_file': SimpleUploadedFile('file.jpg', 'file_content'),
                'run_type': 'a', 'query_type': 'title', 'feedback_type': 'none'}
        response = self.client.post('/task/1/submit/', data)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response,
                            'There was a problem evaluating your results file')

    def test_good_file(self):
        'Should render trec/run.html.'
        self.set_up_user()
        data = {'name': 'run',
                'results_file': open(os.path.join(MEDIA_ROOT, 'results',
                                                  'ap.trec.bm25.0.50.res'))}
        response = self.client.post('/task/1/submit/', data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('trec/run.html')
