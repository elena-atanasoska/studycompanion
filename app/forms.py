from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import modelformset_factory

from .models import CustomUser, Assignment, Task, Reminder, Question


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'name', 'surname')


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

#
# class AssignmentTaskForm(forms.ModelForm):
#     task_name = forms.CharField(max_length=200)
#     is_finished = forms.BooleanField(required=False, widget=forms.CheckboxInput)
#
#     def __init__(self, *args, **kwargs):
#         super(AssignmentTaskForm, self).__init__(*args, **kwargs)
#         for field in self.visible_fields():
#             field.field.widget.attrs["class"] = "form-control"
#
#     class Meta:
#         model = Assignment
#         fields = '__all__'
#
#     def as_bootstrap(self):
#         for name, field in self.fields.items():
#             if isinstance(field.widget, forms.CheckboxInput):
#                 field.widget.attrs['class'] = 'form-check-input'
#             else:
#                 field.widget.attrs['class'] = 'form-control'
#         return self

#
# TaskFormSet = modelformset_factory(Task, fields=('name',), extra=0)


class AssignmentForm(forms.ModelForm):
    tasks = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
        self.fields['name'].widget.attrs['placeholder'] = 'e.g. Assignment 1'
        self.fields['description'].widget.attrs['placeholder'] = 'e.g. You are supposed to solve...'

    def as_bootstrap(self):
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
        return self

    class Meta:
        model = Assignment
        fields = ('name', 'course', 'description', 'progress', 'due_date')


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

    def __init__(self, *args, **kwargs):
        super(ReminderForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
        self.fields['name'].widget.attrs['placeholder'] = 'e.g. Reminder 1'
        self.fields['description'].widget.attrs['placeholder'] = 'e.g. Submit homework assignment "Neural Networks" '


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'course', 'description']

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'is_finished']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class TaskAssignmentForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'is_finished', 'assignment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
