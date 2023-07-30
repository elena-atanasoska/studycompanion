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
    def __init__(self, *args, **kwargs):
        super(AssignmentTaskForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Assignment
        fields = '__all__'

    task_name = forms.CharField(max_length=200)
    is_finished = forms.BooleanField(required=False)

    def as_bootstrap(self):
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
        return self

#
# TaskFormSet = modelformset_factory(Task, fields=('name',), extra=0)
