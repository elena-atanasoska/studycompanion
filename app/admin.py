from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'name', 'surname', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('name', 'surname')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )


admin.site.unregister(Group)
admin.site.register(CustomUser, CustomUserAdmin)


class AdminUsersGroup(GroupAdmin):
    pass


admin.site.register(Group, AdminUsersGroup)
