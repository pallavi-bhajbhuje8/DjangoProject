from django.db import models
from django.contrib.auth.models import User


class HealthMetric(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_metrics')
    date = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                  help_text='Weight in kg')
    heart_rate = models.PositiveIntegerField(null=True, blank=True,
                                              help_text='Resting heart rate (bpm)')
    blood_pressure_systolic = models.PositiveIntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.PositiveIntegerField(null=True, blank=True)
    sleep_hours = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    water_intake = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True,
                                       help_text='Water intake in liters')
    body_fat = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True,
                                    help_text='Body fat percentage')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user.username} - Health Metrics on {self.date}"

    @property
    def blood_pressure(self):
        if self.blood_pressure_systolic and self.blood_pressure_diastolic:
            return f"{self.blood_pressure_systolic}/{self.blood_pressure_diastolic}"
        return "N/A"

    @property
    def bmi(self):
        if self.weight and hasattr(self.user, 'profile') and self.user.profile.height:
            height_m = float(self.user.profile.height) / 100
            if height_m > 0:
                return round(float(self.weight) / (height_m ** 2), 1)
        return None