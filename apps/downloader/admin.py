# coding=utf-8
from django.contrib import admin
from .models import File, FileCategory


class FileAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'uptime', 'category', 'extra_options']
    ordering = ['addition_time']
    search_fields = ['addition_time']


class FileCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code_name', 'is_active']

admin.site.register(File, FileAdmin)
admin.site.register(FileCategory, FileCategoryAdmin)