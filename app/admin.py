from django.contrib import admin

# Register your models here.
from app.models import *
from django.contrib.auth.admin import UserAdmin

# class CustomUserAdmin(UserAdmin):
#     list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_active')

# Register your custom user model with the custom admin class
admin.site.register(CustomUser)
admin.site.register(Comment)