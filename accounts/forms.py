
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class GuideSignUpForm(UserCreationForm):
    '''first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    password1 = forms.CharField(max_length=100)
    password2 = forms.CharField(max_length=100)'''

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name', 'email', 'password1', 'password2')


class StudentSignUpForm(UserCreationForm):
    '''first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    password1 = forms.CharField(max_length=100)
    password2 = forms.CharField(max_length=100)'''

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name', 'email', 'password1', 'password2')
