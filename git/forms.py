from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from git.models import User


# USER REGISTRATION FORM
class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ("username", "password1", "password2")


# USER LOGIN FORM
class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    model = User
    fields = ("username", "password")

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("INVALID LOGIN")
