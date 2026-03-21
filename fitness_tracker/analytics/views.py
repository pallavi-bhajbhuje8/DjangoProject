from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg
from datetime import datetime, timedelta
from workouts.models import Workout
from health_metrics.models import HealthMetric
from meals.models import Meal
from goals.models import Goal
import json


@login_required
def analytics_view(request):
    today = datetime.now().date()
    thirty_days_ago = today - timedelta(days=30)
    seven_days_ago = today - timedelta(days=7)

    # Weekly workout summary
    weekly_workouts = Workout.objects.filter(
        user=request.user,
        date__gte=seven_days_ago
    )
    weekly_workout_count = weekly_workouts.count()
    weekly_duration = weekly_workouts.aggregate(total=Sum('duration'))['total'] or 0
    weekly_calories = weekly_workouts.aggregate(total=Sum('calories_burned'))['total'] or 0

    # Monthly workout summary
    monthly_workouts = Workout.objects.filter(
        user=request.user,
        date__gte=thirty_days_ago
    )
    monthly_workout_count = monthly_workouts.count()
    monthly_duration = monthly_workouts.aggregate(total=Sum('duration'))['total'] or 0
    monthly_calories = monthly_workouts.aggregate(total=Sum('calories_burned'))['total'] or 0

    # Workout frequency by type
    workout_by_type = monthly_workouts.values('workout_type').annotate(
        count=Count('id'),
        total_duration=Sum('duration'),
        total_calories=Sum('calories_burned')
    ).order_by('-count')

    workout_type_labels = []
    workout_type_counts = []
    workout_type_colors = []
    type_colors = {
        'running': '#e74c3c', 'cycling': '#3498db', 'gym': '#2ecc71',
        'yoga': '#9b59b6', 'swimming': '#1abc9c', 'walking': '#f39c12',
        'hiit': '#e67e22', 'stretching': '#1abc9c', 'other': '#95a5a6'
    }

    for wt in workout_by_type:
        workout_type_labels.append(wt['workout_type'].replace('_', ' ').title())
        workout_type_counts.append(wt['count'])
        workout_type_colors.append(type_colors.get(wt['workout_type'], '#95a5a6'))

    # Daily calories burned - last 30 days
    daily_calories_data = []
    daily_labels = []
    for i in range(29, -1, -1):
        day = today - timedelta(days=i)
        daily_labels.append(day.strftime('%b %d'))
        day_calories = Workout.objects.filter(
            user=request.user,
            date=day
        ).aggregate(total=Sum('calories_burned'))['total'] or 0
        daily_calories_data.append(day_calories)

    # Weight progress - last 30 days
    weight_metrics = HealthMetric.objects.filter(
        user=request.user,
        date__gte=thirty_days_ago,
        weight__isnull=False
    ).order_by('date')

    weight_dates = [m.date.strftime('%b %d') for m in weight_metrics]
    weight_values = [float(m.weight) for m in weight_metrics]

    # Weekly workout duration data
    weekly_duration_data = []
    weekly_labels = []
    for i in range(3, -1, -1):
        week_start = today - timedelta(weeks=i, days=today.weekday())
        week_end = week_start + timedelta(days=6)
        weekly_labels.append(week_start.strftime('%b %d'))
        week_dur = Workout.objects.filter(
            user=request.user,
            date__gte=week_start,
            date__lte=week_end
        ).aggregate(total=Sum('duration'))['total'] or 0
        weekly_duration_data.append(week_dur)

    # Meal analytics
    daily_meal_calories = Meal.objects.filter(
        user=request.user,
        date=today
    ).aggregate(total=Sum('calories'))['total'] or 0

    avg_daily_calories = Meal.objects.filter(
        user=request.user,
        date__gte=seven_days_ago
    ).values('date').annotate(
        daily_total=Sum('calories')
    ).aggregate(avg=Avg('daily_total'))['avg'] or 0

    # Goal statistics
    active_goals = Goal.objects.filter(user=request.user, status='active').count()
    completed_goals = Goal.objects.filter(user=request.user, status='completed').count()
    total_goals = Goal.objects.filter(user=request.user).count()

    context = {
        'weekly_workout_count': weekly_workout_count,
        'weekly_duration': weekly_duration,
        'weekly_calories': weekly_calories,
        'monthly_workout_count': monthly_workout_count,
        'monthly_duration': monthly_duration,
        'monthly_calories': monthly_calories,
        'workout_by_type': workout_by_type,
        'workout_type_labels': json.dumps(workout_type_labels),
        'workout_type_counts': json.dumps(workout_type_counts),
        'workout_type_colors': json.dumps(workout_type_colors),
        'daily_labels': json.dumps(daily_labels),
        'daily_calories_data': json.dumps(daily_calories_data),
        'weight_dates': json.dumps(weight_dates),
        'weight_values': json.dumps(weight_values),
        'weekly_labels': json.dumps(weekly_labels),
        'weekly_duration_data': json.dumps(weekly_duration_data),
        'daily_meal_calories': daily_meal_calories,
        'avg_daily_calories': round(avg_daily_calories, 0),
        'active_goals': active_goals,
        'completed_goals': completed_goals,
        'total_goals': total_goals,
    }
    return render(request, 'analytics/analytics.html', context)
