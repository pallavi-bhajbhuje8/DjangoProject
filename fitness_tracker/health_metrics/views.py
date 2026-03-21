from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from .models import HealthMetric
from .forms import HealthMetricForm
import json


@login_required
def metrics_list(request):
    metrics = HealthMetric.objects.filter(user=request.user)

    paginator = Paginator(metrics, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Chart data - last 30 days
    thirty_days_ago = datetime.now().date() - timedelta(days=30)
    chart_metrics = HealthMetric.objects.filter(
        user=request.user,
        date__gte=thirty_days_ago
    ).order_by('date')

    weight_data = []
    sleep_data = []
    heart_rate_data = []
    dates = []

    for m in chart_metrics:
        dates.append(m.date.strftime('%b %d'))
        weight_data.append(float(m.weight) if m.weight else None)
        sleep_data.append(float(m.sleep_hours) if m.sleep_hours else None)
        heart_rate_data.append(m.heart_rate if m.heart_rate else None)

    context = {
        'page_obj': page_obj,
        'dates_json': json.dumps(dates),
        'weight_data_json': json.dumps(weight_data),
        'sleep_data_json': json.dumps(sleep_data),
        'heart_rate_data_json': json.dumps(heart_rate_data),
    }
    return render(request, 'health_metrics/metrics_list.html', context)


@login_required
def metrics_create(request):
    if request.method == 'POST':
        form = HealthMetricForm(request.POST)
        if form.is_valid():
            metric = form.save(commit=False)
            metric.user = request.user
            metric.save()

            # Update profile weight
            if metric.weight:
                profile = request.user.profile
                profile.weight = metric.weight
                profile.save()

            messages.success(request, 'Health metrics logged successfully!')
            return redirect('health_metrics:list')
    else:
        form = HealthMetricForm(initial={'date': datetime.now().date()})

    return render(request, 'health_metrics/metrics_form.html', {
        'form': form,
        'title': 'Log Health Metrics'
    })


@login_required
def metrics_edit(request, pk):
    metric = get_object_or_404(HealthMetric, pk=pk, user=request.user)

    if request.method == 'POST':
        form = HealthMetricForm(request.POST, instance=metric)
        if form.is_valid():
            form.save()
            messages.success(request, 'Health metrics updated successfully!')
            return redirect('health_metrics:list')
    else:
        form = HealthMetricForm(instance=metric)

    return render(request, 'health_metrics/metrics_form.html', {
        'form': form,
        'title': 'Edit Health Metrics',
        'metric': metric
    })


@login_required
def metrics_delete(request, pk):
    metric = get_object_or_404(HealthMetric, pk=pk, user=request.user)
    if request.method == 'POST':
        metric.delete()
        messages.success(request, 'Health metrics deleted.')
        return redirect('health_metrics:list')
    return redirect('health_metrics:list')