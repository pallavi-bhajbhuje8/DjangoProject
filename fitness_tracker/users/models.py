from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    FITNESS_GOAL_CHOICES = [
        ('lose_weight', 'Lose Weight'),
        ('gain_muscle', 'Gain Muscle'),
        ('maintain', 'Maintain Weight'),
        ('improve_endurance', 'Improve Endurance'),
        ('flexibility', 'Improve Flexibility'),
        ('general', 'General Fitness'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                  help_text='Height in cm')
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                  help_text='Weight in kg')
    fitness_goal = models.CharField(max_length=20, choices=FITNESS_GOAL_CHOICES,
                                     default='general')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    daily_step_goal = models.PositiveIntegerField(default=10000)
    daily_calorie_goal = models.PositiveIntegerField(default=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def bmi(self):
        if self.height and self.weight and self.height > 0:
            height_m = float(self.height) / 100
            return round(float(self.weight) / (height_m ** 2), 1)
        return None

    @property
    def bmi_category(self):
        bmi = self.bmi
        if bmi is None:
            return 'N/A'
        if bmi < 18.5:
            return 'Underweight'
        elif bmi < 25:
            return 'Normal'
        elif bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'


class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    date = models.DateField()
    steps = models.PositiveIntegerField(default=0)
    calories_burned = models.PositiveIntegerField(default=0)
    active_minutes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()