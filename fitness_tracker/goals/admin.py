from django.contrib import admin
from .models import Goal


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'goal_type', 'target_value', 'current_value',
                    'progress_percentage', 'status', 'end_date']
    list_filter = ['goal_type', 'status']
    search_fields = ['user__username', 'title']
