from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum
from datetime import datetime, timedelta
from .models import Meal
from .forms import MealForm


@login_required
def meal_list(request):
    meals = Meal.objects.filter(user=request.user)

    # Filter by date
    selected_date = request.GET.get('date')
    if selected_date:
        meals = meals.filter(date=selected_date)
    else:
        selected_date = datetime.now().date().isoformat()
        meals = meals.filter(date=datetime.now().date())

    # Filter by meal time
    meal_time = request.GET.get('meal_time')
    if meal_time:
        meals = meals.filter(meal_time=meal_time)

    # Daily summary
    daily_summary = meals.aggregate(
        total_calories=Sum('calories'),
        total_protein=Sum('protein'),
        total_carbs=Sum('carbs'),
        total_fat=Sum('fat'),
    )

    paginator = Paginator(meals, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'daily_summary': daily_summary,
        'selected_date': selected_date,
        'meal_time_choices': Meal.MEAL_TIME_CHOICES,
        'selected_meal_time': meal_time,
    }
    return render(request, 'meals/meal_list.html', context)


@login_required
def meal_create(request):
    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            messages.success(request, 'Meal logged successfully!')
            return redirect('meals:list')
    else:
        form = MealForm(initial={'date': datetime.now().date()})

    return render(request, 'meals/meal_form.html', {
        'form': form,
        'title': 'Log Meal'
    })


@login_required
def meal_edit(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)

    if request.method == 'POST':
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Meal updated successfully!')
            return redirect('meals:list')
    else:
        form = MealForm(instance=meal)

    return render(request, 'meals/meal_form.html', {
        'form': form,
        'title': 'Edit Meal',
        'meal': meal
    })


@login_required
def meal_delete(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    if request.method == 'POST':
        meal.delete()
        messages.success(request, 'Meal deleted.')
        return redirect('meals:list')
    return redirect('meals:list')