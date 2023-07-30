from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import modelformset_factory

from .models import CustomUser, Assignment, Task


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'name', 'surname')


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class AssignmentTaskForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = '__all__'

    task_name = forms.CharField(max_length=200)
    is_finished = forms.BooleanField(required=False)

#
# TaskFormSet = modelformset_factory(Task, fields=('name',), extra=0)
