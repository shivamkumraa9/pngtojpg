from users.models import MyUser
from django.contrib.auth.forms import UserCreationForm

from django import forms

class LoginForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput())


class PasswordValidationForm(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput())



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ("username","email")
