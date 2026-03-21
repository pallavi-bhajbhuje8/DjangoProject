from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Goal(models.Model):
    GOAL_TYPES = [
        ('daily_steps', 'Daily Steps'),
        ('weekly_workouts', 'Weekly Workouts'),
        ('weight_loss', 'Weight Loss'),
        ('weight_gain', 'Weight Gain'),
        ('calorie_burn', 'Calorie Burn'),
        ('running_distance', 'Running Distance'),
        ('sleep_hours', 'Sleep Hours'),
        ('water_intake', 'Water Intake'),
        ('custom', 'Custom Goal'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    target_value = models.DecimalField(max_digits=10, decimal_places=2)
    current_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit = models.CharField(max_length=20, default='units')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    @property
    def progress_percentage(self):
        if self.target_value and float(self.target_value) > 0:
            return min(round((float(self.current_value) / float(self.target_value)) * 100, 1), 100)
        return 0

    @property
    def is_overdue(self):
        return self.end_date < timezone.now().date() and self.status == 'active'

    @property
    def days_remaining(self):
        delta = self.end_date - timezone.now().date()
        return max(delta.days, 0)

    @property
    def progress_color(self):
        pct = self.progress_percentage
        if pct >= 100:
            return 'success'
        elif pct >= 75:
            return 'info'
        elif pct >= 50:
            return 'warning'
        else:
            return 'danger'
