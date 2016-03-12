from django import forms
from django.contrib.auth.models import User
from trec.models import Researcher

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class ResearcherForm(forms.ModelForm):
    class Meta:
        model = Researcher
        fields = ('profile_pic', 'website', 'display_name', 'organisation')
