from datetime import datetime, timedelta, date

from django.contrib.auth.decorators import login_required
from django.db.models import F, ExpressionWrapper
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout as auth_logout
# from .forms import CustomUserCreationForm, CustomAuthenticationForm, AssignmentTaskForm, ReminderForm, QuestionForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ReminderForm, QuestionForm, AssignmentForm, \
    TaskForm, TaskAssignmentForm
from urllib.parse import urlparse
from django.contrib import messages
# Create your views here.
from app.models import Comment, Assignment, Task, Reminder, Question, CustomUser
import logging
from datetime import date

def your_view(request):
    user = get_object_or_404(CustomUser, id=int(request.user.id)) if request.user.is_authenticated else None

    current_date = date.today()
    current_datetime = timezone.now()

    active_assignments = Assignment.objects.filter(user=user, due_date__gte=current_date)
    active_reminders = Reminder.objects.filter(user=user, deadline__gt=current_datetime)

    nearest_reminder = active_reminders.order_by('deadline').first() if active_reminders.exists() else None

    assignment_least_progress = active_assignments.order_by('progress').first() if active_assignments.exists() else None
    assignment_most_progress = active_assignments.order_by('-progress').first() if active_assignments.exists() else None

    return render(request, 'index.html',
                  {'user': request.user, 'assignment_least_progress': assignment_least_progress,
                   'assignment_most_progress': assignment_most_progress, 'nearest_reminder': nearest_reminder})

def user_logout(request):
    auth_logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Login failed. Please check your credentials and try again.')
        else:
            messages.error(request, 'Login failed. Please check the form and try again.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def assignments_all(request):
    current_datetime = timezone.now()
    user = request.user
    upcoming_assignments = Assignment.objects.filter(user=user, due_date__gt=current_datetime).order_by('due_date')
    past_assignments = Assignment.objects.filter(user=user, due_date__lte=current_datetime).order_by('-due_date')

    tasks = Task.objects.all()
    context = {"upcoming_assignments": upcoming_assignments, "past_assignments": past_assignments, "tasks": tasks}
    return render(request, "assignments.html", context=context)


def add_assignment_task(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.user = request.user  # Assuming you're using authentication
            assignment.save()

            tasks_text = form.cleaned_data.get('tasks', '')
            task_names = [task.strip() for task in tasks_text.split('\n') if task.strip()]
            for task_name in task_names:
                Task.objects.create(name=task_name, assignment=assignment)

            messages.success(request, 'Assignment added successfully.')
            return redirect('assignments')  # Redirect to the list of assignments
    else:
        form = AssignmentForm()

    return render(request, 'add_assignment_task.html', {'form': form, 'today_date': date.today()})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def assignment_details(request, name):
    assignment = get_object_or_404(Assignment, id=name)
    tasks = Task.objects.filter(assignment=assignment)

    if not assignment.user == request.user:
        return redirect('access_denied')

    source = None
    referer = request.META.get('HTTP_REFERER')
    if referer:
        parsed_url = urlparse(referer)
        source = parsed_url.path

    context = {"assignment": assignment, "tasks": tasks, "source": source}
    return render(request, "assignment_details.html", context=context)


def access_denied(request):
    return render(request, "access_denied.html")


@login_required
def delete_assignment(request, name):
    assignment = get_object_or_404(Assignment, id=name)

    if not assignment.user == request.user:
        return redirect('access_denied')

    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Assignment deleted successfully.')
        return redirect('assignments')

    return render(request, 'delete_assignment.html', {'assignment': assignment})


@login_required
def reminders_all(request):
    user = request.user
    current_datetime = timezone.now()
    active_reminders = Reminder.objects.filter(user=user, deadline__gt=current_datetime).order_by('deadline')
    expired_reminders = Reminder.objects.filter(user=user, deadline__lte=current_datetime).order_by('deadline')

    return render(request, 'reminders.html',
                  {'active_reminders': active_reminders, 'expired_reminders': expired_reminders})


def add_reminder(request):
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)

            reminder.user = request.user

            reminder.save()

            messages.success(request, 'Reminder added successfully.')
            return redirect('reminders')
    else:
        form = ReminderForm()

    return render(request, 'add_reminder.html', {'form': form, 'today_date': datetime.now()})


def reminder_details(request, name):
    reminder = get_object_or_404(Reminder, id=name)

    if not reminder.user == request.user:
        return redirect('access_denied')

    source = None
    referer = request.META.get('HTTP_REFERER')
    if referer:
        parsed_url = urlparse(referer)
        source = parsed_url.path

    context = {"reminder": reminder, "source": source}
    return render(request, "reminder_details.html", context=context)


def delete_reminder(request, name):
    reminder = get_object_or_404(Reminder, id=name)

    if not reminder.user == request.user:
        return redirect('access_denied')

    if request.method == 'POST':
        reminder.delete()
        messages.success(request, 'Reminder deleted successfully.')
        return redirect('reminders')

    return render(request, 'delete_reminder.html', {'reminder': reminder})


def edit_reminder(request, name=None):
    reminder = get_object_or_404(Reminder, id=name)

    if not reminder.user == request.user:
        return redirect('access_denied')

    if request.method == 'POST':
        form = ReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()

            messages.success(request, 'Reminder edited successfully.')
            return redirect('reminders')
    else:
        form = ReminderForm(instance=reminder)

    return render(request, 'edit_reminder.html', {'form': form, 'reminder': reminder})


def edit_assignment(request, name=None):
    assignment = get_object_or_404(Assignment, id=name)

    if not assignment.user == request.user:
        return redirect('access_denied')

    tasks = assignment.tasks.all()

    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            tasks_text = form.cleaned_data.get('tasks', '')
            task_names = [task.strip() for task in tasks_text.split('\n') if task.strip()]
            Task.objects.filter(assignment=assignment).delete()  # Delete existing tasks
            for task_name in task_names:
                Task.objects.create(name=task_name, assignment=assignment)
            form.save()
            messages.success(request, 'Assignment edited successfully.')
            return redirect('assignments')
    else:
        form = AssignmentForm(instance=assignment)

    return render(request, 'edit_assignment.html', {'form': form, 'assignment': assignment, 'tasks': tasks})


def group_study(request):
    questions = Question.objects.all()
    return render(request, 'group_study.html', {'questions': questions})


def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            messages.success(request, 'Your question was posted.')
            return redirect('group_study')  # Redirect to the group study page after asking a question
    else:
        form = QuestionForm()

    return render(request, 'ask_question.html', {'form': form})


def chat(request):
    return render(request, "chat.html")


def edit_task(request, name):
    task = get_object_or_404(Task, id=name)

    if not task.assignment.user == request.user:
        return redirect('access_denied')

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task edited successfully.')
            return redirect('assignments')
    else:
        form = TaskForm(instance=task)

    context = {'form': form, 'task': task}
    return render(request, 'edit_task.html', context)


def delete_task(request, name):
    task = get_object_or_404(Task, id=name)

    if not task.assignment.user == request.user:
        return redirect('access_denied')

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('assignments')

    return render(request, 'delete_task.html', {'task': task})


def task_details(request, task_name):
    task = get_object_or_404(Task, id=task_name)

    if not task.assignment.user == request.user:
        return redirect('access_denied')

    context = {'task': task}
    return render(request, 'task_details.html', context)


def add_task(request):
    if request.method == 'POST':
        form = TaskAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task added successfully.')
            return redirect('assignments')
    else:
        form = TaskAssignmentForm()

    context = {'form': form}
    return render(request, 'add_task.html', context)
