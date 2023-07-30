from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm, AssignmentTaskForm

# Create your views here.
from app.models import Comment, Assignment, Task


def your_view(request):
    comments = Comment.objects.all()
    current_date = datetime.now().date()
    end_date_limit = current_date + timedelta(days=5)
    assignments = Assignment.objects.filter(due_date__lte=end_date_limit)
    return render(request, 'index.html', {'comments': comments, 'user': request.user, 'assignments': assignments})


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
    context = {"assignment":assignment}
    return render(request, "assignment_details.html", context=context)

def delete_assignment(request, name):
    assignment = Assignment.objects.get(name=name)
    if request.method == 'POST':
        assignment.delete()
        return redirect('assignments')
    return render(request, 'delete_assignment.html', {'assignment': assignment})