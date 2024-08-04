from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile


# Register your models here.

# TODO: implement MyUserAdmin without 'username'
admin.site.register(UserProfile, UserAdmin)
