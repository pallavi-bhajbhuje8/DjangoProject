from django.contrib import admin
from .models import Meal


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ['user', 'meal_name', 'calories', 'protein', 'carbs', 'fat',
                    'meal_time', 'date']
    list_filter = ['meal_time', 'date']
    search_fields = ['user__username', 'meal_name']
    date_hierarchy = 'date'