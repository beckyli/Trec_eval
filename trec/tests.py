from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase

from populate_trec import add_researcher

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

    def test_get_request(self):
        'Both forms should be displayed.'
        researcher = add_researcher('jill')
        self.client.login(username='jill', password='jill')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('user_form', response.context)
        self.assertIn('researcher_form', response.context)
