from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Workout
from .forms import WorkoutForm


@login_required
def workout_list(request):
    workouts = Workout.objects.filter(user=request.user)

    # Filter by workout type
    workout_type = request.GET.get('type')
    if workout_type:
        workouts = workouts.filter(workout_type=workout_type)

    # Filter by intensity
    intensity = request.GET.get('intensity')
    if intensity:
        workouts = workouts.filter(intensity=intensity)

    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        workouts = workouts.filter(date__gte=date_from)
    if date_to:
        workouts = workouts.filter(date__lte=date_to)

    # Search
    search = request.GET.get('search')
    if search:
        workouts = workouts.filter(notes__icontains=search)

    paginator = Paginator(workouts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'workout_types': Workout.WORKOUT_TYPES,
        'intensity_choices': Workout.INTENSITY_CHOICES,
        'selected_type': workout_type,
        'selected_intensity': intensity,
    }
    return render(request, 'workouts/workout_list.html', context)


@login_required
def workout_create(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            messages.success(request, 'Workout logged successfully!')
            return redirect('workouts:list')
    else:
        form = WorkoutForm()

    return render(request, 'workouts/workout_form.html', {
        'form': form,
        'title': 'Log New Workout'
    })


@login_required
def workout_detail(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    return render(request, 'workouts/workout_detail.html', {'workout': workout})


@login_required
def workout_edit(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)

    if request.method == 'POST':
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            messages.success(request, 'Workout updated successfully!')
            return redirect('workouts:detail', pk=pk)
    else:
        form = WorkoutForm(instance=workout)

    return render(request, 'workouts/workout_form.html', {
        'form': form,
        'title': 'Edit Workout',
        'workout': workout
    })


@login_required
def workout_delete(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)

    if request.method == 'POST':
        workout.delete()
        messages.success(request, 'Workout deleted successfully!')
        return redirect('workouts:list')

    return render(request, 'workouts/workout_detail.html', {
        'workout': workout,
        'confirm_delete': True
    })