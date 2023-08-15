"""
URL configuration for studycompanion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.your_view, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('assignments/', views.assignments_all, name='assignments'),
    path('assignments/add/', views.add_assignment_task, name='add_assignment_task'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('assignments/details/<str:name>', views.assignment_details, name='assignment_details'),
    path('delete_assignment/<str:name>', views.delete_assignment, name='delete_assignment'),
    path('reminders/', views.reminders_all, name='reminders'),
    path('reminders/add', views.add_reminder, name='add_reminder'),
    path('reminder/details/<str:name>', views.reminder_details, name='reminder_details'),
    path('delete_reminder/<str:name>', views.delete_reminder, name='delete_reminder'),
    path('edit_reminder/<str:name>', views.edit_reminder, name='edit_reminder'),
    path('edit_assignment/<str:name>', views.edit_assignment, name='edit_assignment'),
    path('group_study/', views.group_study, name='group_study'),
    path('ask_question/', views.ask_question, name='ask_question'),
    path('reminder_details/<str:name>/<str:source>/', views.reminder_details, name='reminder_details'),
    path('assignment_details/<str:name>/<str:source>/', views.assignment_details, name='assignment_details'),
    path('chat/', views.chat, name='chat'),
    path('task_details/<str:task_name>/', views.task_details, name='task_details'),
    path('edit_task/<str:name>/', views.edit_task, name='edit_task'),
    path('delete_task/<str:name>/', views.delete_task, name='delete_task'),
    path('add_task/', views.add_task, name='add_task'),
    path('access-denied/', views.access_denied, name='access_denied'),
]
