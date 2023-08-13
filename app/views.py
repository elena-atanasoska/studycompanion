from datetime import datetime, timedelta
from django.db.models import F, ExpressionWrapper
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm, AssignmentTaskForm, ReminderForm, QuestionForm
from urllib.parse import urlparse

# Create your views here.
from app.models import Comment, Assignment, Task, Reminder, Question


def your_view(request):
    comments = Comment.objects.all()
    current_date = datetime.now().date()
    current_datetime = timezone.now()
    end_date_limit = current_date + timedelta(days=5)
    assignments = Assignment.objects.filter(due_date__lte=end_date_limit)
    active_reminders = Reminder.objects.filter(deadline__gt=current_datetime)

    nearest_reminder = active_reminders.order_by('deadline').first() if active_reminders.exists() else None
    assignment_least_progress = assignments.order_by('progress').first() if assignments.exists() else None
    assignment_most_progress = assignments.order_by('-progress').first() if assignments.exists() else None

    return render(request, 'index.html', {'comments': comments, 'user': request.user, 'assignments': assignments, 'nearest_reminder':nearest_reminder,  'assignment_least_progress': assignment_least_progress,
        'assignment_most_progress': assignment_most_progress,})


def user_logout(request):
    auth_logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
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
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def assignments_all(request):
    queryset = Assignment.objects.all()
    context = {"assignments": queryset}
    return render(request, "assignments.html", context=context)


def add_assignment_task(request):
    if request.method == 'POST':
        form = AssignmentTaskForm(request.POST)

        if form.is_valid():
            assignment = form.save()
            task_name = form.cleaned_data['task_name']
            is_finished = form.cleaned_data['is_finished']

            # Create the task and associate it with the assignment
            task = Task(name=task_name, is_finished=is_finished, assignment=assignment)
            task.save()

            return redirect(
                'assignments')  # Replace 'assignment_list' with your actual view name for listing assignments

    else:
        form = AssignmentTaskForm()

    return render(request, 'add_assignment_task.html', {'form': form})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def assignment_details(request, name):
    assignment = Assignment.objects.get(name=name)
    source = None
    referer = request.META.get('HTTP_REFERER')
    if referer:
        parsed_url = urlparse(referer)
        source = parsed_url.path

    context = {"assignment": assignment, "source": source}
    return render(request, "assignment_details.html", context=context)


def delete_assignment(request, name):
    assignment = Assignment.objects.get(name=name)
    if request.method == 'POST':
        assignment.delete()
        return redirect('assignments')
    return render(request, 'delete_assignment.html', {'assignment': assignment})


def reminders_all(request):
    reminders = Reminder.objects.all()
    return render(request, 'reminders.html', {'reminders': reminders})


def add_reminder(request):
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reminders')  # Replace 'reminder_list' with the URL name for your reminder list view
    else:
        form = ReminderForm()

    return render(request, 'add_reminder.html', {'form': form})


def reminder_details(request, name):
    reminder = Reminder.objects.get(name=name)
    source = None
    referer = request.META.get('HTTP_REFERER')
    if referer:
        parsed_url = urlparse(referer)
        source = parsed_url.path

    context = {"reminder": reminder, "source": source}
    return render(request, "reminder_details.html", context=context)


def delete_reminder(request, name):
    reminder = Reminder.objects.get(name=name)
    if request.method == 'POST':
        reminder.delete()
        return redirect('reminders')
    return render(request, 'delete_reminder.html', {'reminder': reminder})


def edit_reminder(request, name=None):
    reminder = Reminder.objects.get(name=name)

    if request.method == 'POST':
        form = ReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            return redirect('reminders')
    else:
        form = ReminderForm(instance=reminder)

    return render(request, 'edit_reminder.html', {'form': form, 'reminder': reminder})


def edit_assignment(request, name=None):
    assignment = Assignment.objects.get(name=name)

    if request.method == 'POST':
        form = AssignmentTaskForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('assignments')
    else:
        form = AssignmentTaskForm(instance=assignment)

    return render(request, 'edit_assignment.html', {'form': form, 'assignment': assignment})


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
            return redirect('group_study')  # Redirect to the group study page after asking a question
    else:
        form = QuestionForm()

    return render(request, 'ask_question.html', {'form': form})


def chat(request):
    return render(request, "chat.html")