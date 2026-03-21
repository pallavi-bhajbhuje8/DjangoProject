from django.db import models
from django.contrib.auth.models import User


class Workout(models.Model):
    WORKOUT_TYPES = [
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('gym', 'Gym'),
        ('yoga', 'Yoga'),
        ('swimming', 'Swimming'),
        ('walking', 'Walking'),
        ('hiit', 'HIIT'),
        ('stretching', 'Stretching'),
        ('other', 'Other'),
    ]

    INTENSITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('extreme', 'Extreme'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    workout_type = models.CharField(max_length=20, choices=WORKOUT_TYPES)
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    distance = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True,
                                    help_text='Distance in km')
    calories_burned = models.PositiveIntegerField(default=0)
    intensity = models.CharField(max_length=10, choices=INTENSITY_CHOICES, default='medium')
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_workout_type_display()} on {self.date}"

    @property
    def workout_icon(self):
        icons = {
            'running': 'bi-person-walking',
            'cycling': 'bi-bicycle',
            'gym': 'bi-trophy',
            'yoga': 'bi-peace',
            'swimming': 'bi-water',
            'walking': 'bi-person-walking',
            'hiit': 'bi-lightning',
            'stretching': 'bi-arrows-angle-expand',
            'other': 'bi-activity',
        }
        return icons.get(self.workout_type, 'bi-activity')

    @property
    def workout_color(self):
        colors = {
            'running': '#e74c3c',
            'cycling': '#3498db',
            'gym': '#2ecc71',
            'yoga': '#9b59b6',
            'swimming': '#1abc9c',
            'walking': '#f39c12',
            'hiit': '#e67e22',
            'stretching': '#1abc9c',
            'other': '#95a5a6',
        }
        return colors.get(self.workout_type, '#95a5a6')
