from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from .models import CustomUser, Assignment, Course, Task, Reminder, Question
from django.forms import BaseInlineFormSet
from django import forms


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'name', 'surname', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('name', 'surname')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )


# admin.site.unregister(Group)
admin.site.register(CustomUser, CustomUserAdmin)


# class AdminUsersGroup(GroupAdmin):
#     pass
#
#
# admin.site.register(Group, AdminUsersGroup)


class CourseAdmin(admin.ModelAdmin):
    list_display = ["name", ]


admin.site.register(Course, CourseAdmin)


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1  # Number of empty task forms to display


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'user', 'progress', 'due_date')
    list_filter = ('course', 'user', 'progress', 'due_date')
    search_fields = ('name', 'user__username')
    inlines = [TaskInline]


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'assignment', 'is_finished')
    list_filter = ('assignment', 'is_finished')
    search_fields = ('name', 'assignment__name')


admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Task, TaskAdmin)


class ReminderAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'course', 'deadline')
    list_filter = ('course', 'deadline')
    search_fields = ('name', 'description')
    ordering = ('deadline',)


admin.site.register(Reminder, ReminderAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'user')
    list_filter = ('course', 'user')
    search_fields = ('title', 'description', 'user__username')
    ordering = ('-id',)  # You can specify the default sorting order


admin.site.register(Question, QuestionAdmin)