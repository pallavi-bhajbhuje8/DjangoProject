from django.contrib import admin
from .models import UserProfile, ActivityLog


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'gender', 'weight', 'height', 'fitness_goal', 'bmi']
    list_filter = ['gender', 'fitness_goal']
    search_fields = ['user__username', 'user__email']


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'steps', 'calories_burned', 'active_minutes']
    list_filter = ['date']
    search_fields = ['user__username']