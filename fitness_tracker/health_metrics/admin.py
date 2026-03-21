from django.contrib import admin
from .models import HealthMetric


@admin.register(HealthMetric)
class HealthMetricAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'weight', 'heart_rate', 'sleep_hours',
                    'water_intake', 'body_fat']
    list_filter = ['date']
    search_fields = ['user__username']
    date_hierarchy = 'date'