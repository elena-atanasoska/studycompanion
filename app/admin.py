from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from .models import CustomUser, Assignment, Course, Task
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


class TaskInline(admin.TabularInline):  # or admin.StackedInline for a different display style
    model = Task
    extra = 1


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'user', 'progress', 'due_date')
    inlines = [TaskInline]
    #
    # def save_model(self, request, obj, form, change):
    #     # Save the Assignment object first
    #     super().save_model(request, obj, form, change)
    #
    #     # Handle tasks for the Assignment
    #     task_data = form.cleaned_data.get('tasks')
    #     if task_data:
    #         task_names = task_data.split(',')  # Assuming task_data is a comma-separated string of task names
    #         tasks = Task.objects.filter(name__in=task_names)
    #         obj.tasks.set(tasks)
    #
    # def get_form(self, request, obj=None, **kwargs):
    #     # Override get_form method to pass the current assignment object to the custom form
    #     form = super().get_form(request, obj, **kwargs)
    #     form.current_assignment = obj
    #     return form
    #
    # def get_formsets_with_inlines(self, request, obj=None):
    #     # Override get_formsets_with_inlines to pass the current assignment object to the inline formset
    #     for inline in self.get_inline_instances(request, obj):
    #         yield inline.get_formset(request, obj), inline


admin.site.register(Assignment, AssignmentAdmin)
