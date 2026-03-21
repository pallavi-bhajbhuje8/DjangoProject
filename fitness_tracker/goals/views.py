from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Goal
from .forms import GoalForm
from datetime import datetime


@login_required
def goal_list(request):
    status_filter = request.GET.get('status', 'active')
    goals = Goal.objects.filter(user=request.user)

    if status_filter and status_filter != 'all':
        goals = goals.filter(status=status_filter)

    context = {
        'goals': goals,
        'status_filter': status_filter,
    }
    return render(request, 'goals/goal_list.html', context)


@login_required
def goal_create(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, 'Goal created successfully!')
            return redirect('goals:list')
    else:
        form = GoalForm(initial={
            'start_date': datetime.now().date(),
            'current_value': 0,
        })

    return render(request, 'goals/goal_form.html', {
        'form': form,
        'title': 'Create New Goal'
    })


@login_required
def goal_edit(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)

    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            goal = form.save()
            if goal.progress_percentage >= 100 and goal.status == 'active':
                goal.status = 'completed'
                goal.save()
            messages.success(request, 'Goal updated successfully!')
            return redirect('goals:list')
    else:
        form = GoalForm(instance=goal)

    return render(request, 'goals/goal_form.html', {
        'form': form,
        'title': 'Edit Goal',
        'goal': goal
    })


@login_required
def goal_delete(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Goal deleted.')
        return redirect('goals:list')
    return redirect('goals:list')