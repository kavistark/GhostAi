from django.contrib import admin
from .models import Mission

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('mission_id', 'title', 'status', 'created_at')
    search_fields = ('mission_id', 'title')
    list_filter = ('status', 'created_at')
