from django.contrib import admin
from .models import Scheme, SchemeApplication


@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'organization', 'status', 'created_by', 'created_at']
    list_filter = ['category', 'status', 'created_at']
    search_fields = ['name', 'description', 'organization']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SchemeApplication)
class SchemeApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'scheme', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['user__username', 'scheme__name']
    readonly_fields = ['applied_at']
