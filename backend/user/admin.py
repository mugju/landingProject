from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin
from .models import Logtbl

@admin.register(Logtbl)
class LogtblAdmin(admin.ModelAdmin):
    list_display = ['action', 'username', 'ip','timestamp',]
    list_filter = ['action','username']