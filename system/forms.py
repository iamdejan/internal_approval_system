from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Employee

class CustomEmployeeCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = ("username", "first_name", "last_name", "password", "level")

class CustomEmployeeChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Employee
        fields = ("username", "first_name", "last_name", "password", "level")