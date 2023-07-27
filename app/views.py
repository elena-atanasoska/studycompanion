from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm

# Create your views here.
from app.models import Comment, Assignment


def your_view(request):
    comments = Comment.objects.all()
    return render(request, 'index.html', {'comments': comments, 'user': request.user})

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
    context = {"assignments" : queryset}
    return render(request, "assignments.html", context = context)

