from django import forms
from django.contrib.auth.models import User
from trec.models import Researcher, Run, Track

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ('username',)

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ('title', 'track_url', 'description', 'genre')

class ResearcherForm(forms.ModelForm):
    class Meta:
        model = Researcher
        fields = ('profile_pic', 'website', 'display_name', 'organisation')

class RunForm(forms.ModelForm):
    class Meta:
        model = Run
        fields = ('name', 'description', 'results_file', 'run_type',
                  'query_type', 'feedback_type')
