from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from workouts.models import Workout
from health_metrics.models import HealthMetric
from goals.models import Goal
from meals.models import Meal
from users.models import ActivityLog
import json


@login_required
def dashboard_view(request):
    today = datetime.now().date()
    seven_days_ago = today - timedelta(days=7)
    thirty_days_ago = today - timedelta(days=30)

    # Today's activity
    today_activity = ActivityLog.objects.filter(
        user=request.user,
        date=today
    ).first()

    today_steps = today_activity.steps if today_activity else 0
    today_active_minutes = today_activity.active_minutes if today_activity else 0

    # Today's calories burned from workouts
    today_calories_workout = Workout.objects.filter(
        user=request.user,
        date=today
    ).aggregate(total=Sum('calories_burned'))['total'] or 0

    today_calories = (today_activity.calories_burned if today_activity else 0) + today_calories_workout

    # Today's workout duration
    today_duration = Workout.objects.filter(
        user=request.user,
        date=today
    ).aggregate(total=Sum('duration'))['total'] or 0

    # Profile data
    profile = request.user.profile
    step_goal = profile.daily_step_goal or 10000
    calorie_goal = profile.daily_calorie_goal or 2000

    step_percentage = min(round((today_steps / step_goal) * 100, 1), 100) if step_goal > 0 else 0

    # Today's meal calories
    today_meal_calories = Meal.objects.filter(
        user=request.user,
        date=today
    ).aggregate(total=Sum('calories'))['total'] or 0

    meal_calorie_percentage = min(
        round((today_meal_calories / calorie_goal) * 100, 1), 100
    ) if calorie_goal > 0 else 0

    # Recent workouts
    recent_workouts = Workout.objects.filter(user=request.user)[:5]

    # Active goals
    active_goals = Goal.objects.filter(user=request.user, status='active')[:4]

    # Goal completion stats
    total_goals = Goal.objects.filter(user=request.user).count()
    completed_goals = Goal.objects.filter(user=request.user, status='completed').count()
    goal_completion_pct = round(
        (completed_goals / total_goals) * 100, 1
    ) if total_goals > 0 else 0

    # Weight progress (last 7 entries)
    weight_history = HealthMetric.objects.filter(
        user=request.user,
        weight__isnull=False
    ).order_by('-date')[:7]

    weight_dates = []
    weight_values = []
    for wh in reversed(list(weight_history)):
        weight_dates.append(wh.date.strftime('%b %d'))
        weight_values.append(float(wh.weight))

    # Weekly workout stats for chart
    weekly_data = []
    weekly_labels = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        weekly_labels.append(day.strftime('%a'))
        day_duration = Workout.objects.filter(
            user=request.user,
            date=day
        ).aggregate(total=Sum('duration'))['total'] or 0
        weekly_data.append(day_duration)

    # This week stats
    week_workouts = Workout.objects.filter(
        user=request.user,
        date__gte=seven_days_ago
    )
    week_workout_count = week_workouts.count()
    week_total_duration = week_workouts.aggregate(total=Sum('duration'))['total'] or 0
    week_total_calories = week_workouts.aggregate(total=Sum('calories_burned'))['total'] or 0

    # Latest health metrics
    latest_metric = HealthMetric.objects.filter(user=request.user).first()

    context = {
        'today_steps': today_steps,
        'step_goal': step_goal,
        'step_percentage': step_percentage,
        'today_calories': today_calories,
        'today_duration': today_duration,
        'today_active_minutes': today_active_minutes,
        'today_meal_calories': today_meal_calories,
        'calorie_goal': calorie_goal,
        'meal_calorie_percentage': meal_calorie_percentage,
        'recent_workouts': recent_workouts,
        'active_goals': active_goals,
        'goal_completion_pct': goal_completion_pct,
        'completed_goals': completed_goals,
        'total_goals': total_goals,
        'weight_dates_json': json.dumps(weight_dates),
        'weight_values_json': json.dumps(weight_values),
        'weekly_labels_json': json.dumps(weekly_labels),
        'weekly_data_json': json.dumps(weekly_data),
        'week_workout_count': week_workout_count,
        'week_total_duration': week_total_duration,
        'week_total_calories': week_total_calories,
        'latest_metric': latest_metric,
        'profile': profile,
    }
    return render(request, 'dashboard/dashboard.html', context)
