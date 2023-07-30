from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import modelformset_factory

from .models import CustomUser, Assignment, Task, Reminder


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


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['name', 'description', 'course', 'deadline']

    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        'course': forms.Select(attrs={'class': 'form-control'}),
        'deadline': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker'}),
    }

