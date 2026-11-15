from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'gender', 'category', 'state', 'education']
    list_filter = ['gender', 'category', 'state', 'education']
    search_fields = ['user__username', 'user__email', 'occupation']
