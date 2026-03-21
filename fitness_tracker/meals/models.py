from django.db import models
from django.contrib.auth.models import User


class Meal(models.Model):
    MEAL_TIME_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
        ('pre_workout', 'Pre-Workout'),
        ('post_workout', 'Post-Workout'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meals')
    meal_name = models.CharField(max_length=200)
    calories = models.PositiveIntegerField(default=0)
    protein = models.DecimalField(max_digits=6, decimal_places=1, default=0,
                                   help_text='Protein in grams')
    carbs = models.DecimalField(max_digits=6, decimal_places=1, default=0,
                                 help_text='Carbs in grams')
    fat = models.DecimalField(max_digits=6, decimal_places=1, default=0,
                               help_text='Fat in grams')
    fiber = models.DecimalField(max_digits=6, decimal_places=1, default=0,
                                 help_text='Fiber in grams')
    meal_time = models.CharField(max_length=20, choices=MEAL_TIME_CHOICES)
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.meal_name} ({self.date})"

    @property
    def total_macros(self):
        return float(self.protein) + float(self.carbs) + float(self.fat)

    @property
    def meal_icon(self):
        icons = {
            'breakfast': 'bi-sunrise',
            'lunch': 'bi-sun',
            'dinner': 'bi-moon-stars',
            'snack': 'bi-cup-hot',
            'pre_workout': 'bi-lightning',
            'post_workout': 'bi-trophy',
        }
        return icons.get(self.meal_time, 'bi-cup-hot')
