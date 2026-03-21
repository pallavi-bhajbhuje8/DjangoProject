# users/management/__init__.py - create empty
# users/management/commands/__init__.py - create empty
# users/management/commands/load_sample_data.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import UserProfile, ActivityLog
from workouts.models import Workout
from health_metrics.models import HealthMetric
from goals.models import Goal
from meals.models import Meal
from datetime import datetime, timedelta
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Load sample data for the fitness tracker application'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create sample user
        user, created = User.objects.get_or_create(
            username='john_fitness',
            defaults={
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'john@example.com',
            }
        )
        if created:
            user.set_password('FitTrack123!')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created user: john_fitness / FitTrack123!'))

        # Update profile
        profile = user.profile
        profile.age = 28
        profile.gender = 'M'
        profile.height = Decimal('178.00')
        profile.weight = Decimal('75.50')
        profile.fitness_goal = 'gain_muscle'
        profile.daily_step_goal = 10000
        profile.daily_calorie_goal = 2500
        profile.save()

        today = datetime.now().date()

        # Create Workouts
        workout_data = [
            {'workout_type': 'running', 'duration': 45, 'distance': Decimal('5.5'),
             'calories_burned': 450, 'intensity': 'high', 'date': today,
             'notes': 'Morning run in the park. Felt great!'},
            {'workout_type': 'gym', 'duration': 60, 'distance': None,
             'calories_burned': 350, 'intensity': 'high', 'date': today - timedelta(days=1),
             'notes': 'Upper body workout - bench press, rows, and shoulder press.'},
            {'workout_type': 'cycling', 'duration': 30, 'distance': Decimal('12.0'),
             'calories_burned': 280, 'intensity': 'medium', 'date': today - timedelta(days=2),
             'notes': 'Easy cycling around the neighborhood.'},
            {'workout_type': 'yoga', 'duration': 40, 'distance': None,
             'calories_burned': 150, 'intensity': 'low', 'date': today - timedelta(days=3),
             'notes': 'Morning yoga session for flexibility.'},
            {'workout_type': 'swimming', 'duration': 35, 'distance': Decimal('1.5'),
             'calories_burned': 320, 'intensity': 'medium', 'date': today - timedelta(days=4),
             'notes': 'Laps at the community pool.'},
            {'workout_type': 'gym', 'duration': 55, 'distance': None,
             'calories_burned': 400, 'intensity': 'high', 'date': today - timedelta(days=5),
             'notes': 'Leg day - squats, deadlifts, leg press.'},
            {'workout_type': 'walking', 'duration': 60, 'distance': Decimal('5.0'),
             'calories_burned': 200, 'intensity': 'low', 'date': today - timedelta(days=6),
             'notes': 'Evening walk with friends.'},
            {'workout_type': 'hiit', 'duration': 25, 'distance': None,
             'calories_burned': 380, 'intensity': 'extreme', 'date': today - timedelta(days=7),
             'notes': 'Intense HIIT circuit training.'},
            {'workout_type': 'running', 'duration': 30, 'distance': Decimal('4.0'),
             'calories_burned': 320, 'intensity': 'medium', 'date': today - timedelta(days=8),
             'notes': 'Interval training on the track.'},
            {'workout_type': 'gym', 'duration': 50, 'distance': None,
             'calories_burned': 300, 'intensity': 'medium', 'date': today - timedelta(days=9),
             'notes': 'Core and abs workout.'},
        ]

        # Add more workouts for the past month
        for i in range(10, 30):
            workout_types = ['running', 'cycling', 'gym', 'yoga', 'walking', 'hiit']
            wt = random.choice(workout_types)
            dur = random.randint(20, 75)
            cal = random.randint(150, 500)
            intensities = ['low', 'medium', 'high']
            workout_data.append({
                'workout_type': wt,
                'duration': dur,
                'distance': Decimal(str(round(random.uniform(1, 15), 1))) if wt in ['running', 'cycling', 'walking'] else None,
                'calories_burned': cal,
                'intensity': random.choice(intensities),
                'date': today - timedelta(days=i),
                'notes': f'Regular {wt} session.'
            })

        for wd in workout_data:
            Workout.objects.get_or_create(
                user=user,
                date=wd['date'],
                workout_type=wd['workout_type'],
                defaults=wd
            )

        self.stdout.write(self.style.SUCCESS(f'Created {len(workout_data)} workouts'))

        # Create Health Metrics
        for i in range(30):
            date = today - timedelta(days=i)
            weight = Decimal(str(round(75.5 - (i * 0.05) + random.uniform(-0.3, 0.3), 2)))
            HealthMetric.objects.get_or_create(
                user=user,
                date=date,
                defaults={
                    'weight': weight,
                    'heart_rate': random.randint(58, 72),
                    'blood_pressure_systolic': random.randint(110, 130),
                    'blood_pressure_diastolic': random.randint(70, 85),
                    'sleep_hours': Decimal(str(round(random.uniform(5.5, 8.5), 1))),
                    'water_intake': Decimal(str(round(random.uniform(1.5, 3.5), 1))),
                    'body_fat': Decimal(str(round(random.uniform(14, 18), 1))),
                }
            )

        self.stdout.write(self.style.SUCCESS('Created 30 days of health metrics'))

        # Create Goals
        goals_data = [
            {
                'goal_type': 'weekly_workouts',
                'title': 'Workout 5 times this week',
                'description': 'Stay consistent with at least 5 workout sessions per week.',
                'target_value': Decimal('5'),
                'current_value': Decimal('3'),
                'unit': 'workouts',
                'start_date': today - timedelta(days=today.weekday()),
                'end_date': today - timedelta(days=today.weekday()) + timedelta(days=6),
                'status': 'active',
            },
            {
                'goal_type': 'running_distance',
                'title': 'Run 50km this month',
                'description': 'Build up running endurance with a monthly target.',
                'target_value': Decimal('50'),
                'current_value': Decimal('32.5'),
                'unit': 'km',
                'start_date': today.replace(day=1),
                'end_date': (today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1),
                'status': 'active',
            },
            {
                'goal_type': 'weight_loss',
                'title': 'Reach 73kg',
                'description': 'Gradual weight loss to reach target weight.',
                'target_value': Decimal('73'),
                'current_value': Decimal('75.5'),
                'unit': 'kg',
                'start_date': today - timedelta(days=30),
                'end_date': today + timedelta(days=60),
                'status': 'active',
            },
            {
                'goal_type': 'calorie_burn',
                'title': 'Burn 10,000 calories this month',
                'description': 'High calorie burn target for fat loss.',
                'target_value': Decimal('10000'),
                'current_value': Decimal('6500'),
                'unit': 'kcal',
                'start_date': today.replace(day=1),
                'end_date': (today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1),
                'status': 'active',
            },
            {
                'goal_type': 'water_intake',
                'title': 'Drink 3L water daily for 2 weeks',
                'description': 'Stay hydrated consistently.',
                'target_value': Decimal('14'),
                'current_value': Decimal('14'),
                'unit': 'days',
                'start_date': today - timedelta(days=20),
                'end_date': today - timedelta(days=6),
                'status': 'completed',
            },
        ]

        for gd in goals_data:
            Goal.objects.get_or_create(
                user=user,
                title=gd['title'],
                defaults=gd
            )

        self.stdout.write(self.style.SUCCESS(f'Created {len(goals_data)} goals'))

        # Create Meals
        meals_data = [
            # Today
            {'meal_name': 'Oatmeal with Berries', 'calories': 350, 'protein': Decimal('12'),
             'carbs': Decimal('55'), 'fat': Decimal('8'), 'fiber': Decimal('6'),
             'meal_time': 'breakfast', 'date': today},
            {'meal_name': 'Grilled Chicken Salad', 'calories': 450, 'protein': Decimal('38'),
             'carbs': Decimal('20'), 'fat': Decimal('18'), 'fiber': Decimal('5'),
             'meal_time': 'lunch', 'date': today},
            {'meal_name': 'Protein Shake', 'calories': 200, 'protein': Decimal('30'),
             'carbs': Decimal('10'), 'fat': Decimal('3'), 'fiber': Decimal('1'),
             'meal_time': 'post_workout', 'date': today},
            {'meal_name': 'Salmon with Rice', 'calories': 550, 'protein': Decimal('35'),
             'carbs': Decimal('50'), 'fat': Decimal('20'), 'fiber': Decimal('3'),
             'meal_time': 'dinner', 'date': today},
            {'meal_name': 'Greek Yogurt', 'calories': 150, 'protein': Decimal('15'),
             'carbs': Decimal('12'), 'fat': Decimal('5'), 'fiber': Decimal('0'),
             'meal_time': 'snack', 'date': today},
            # Yesterday
            {'meal_name': 'Scrambled Eggs & Toast', 'calories': 400, 'protein': Decimal('22'),
             'carbs': Decimal('35'), 'fat': Decimal('18'), 'fiber': Decimal('3'),
             'meal_time': 'breakfast', 'date': today - timedelta(days=1)},
            {'meal_name': 'Turkey Sandwich', 'calories': 380, 'protein': Decimal('28'),
             'carbs': Decimal('40'), 'fat': Decimal('12'), 'fiber': Decimal('4'),
             'meal_time': 'lunch', 'date': today - timedelta(days=1)},
            {'meal_name': 'Steak with Vegetables', 'calories': 600, 'protein': Decimal('45'),
             'carbs': Decimal('25'), 'fat': Decimal('28'), 'fiber': Decimal('6'),
             'meal_time': 'dinner', 'date': today - timedelta(days=1)},
        ]

        for md in meals_data:
            Meal.objects.get_or_create(
                user=user,
                meal_name=md['meal_name'],
                date=md['date'],
                defaults=md
            )

        self.stdout.write(self.style.SUCCESS(f'Created {len(meals_data)} meals'))

        # Create Activity Logs
        for i in range(14):
            date = today - timedelta(days=i)
            ActivityLog.objects.get_or_create(
                user=user,
                date=date,
                defaults={
                    'steps': random.randint(5000, 15000),
                    'calories_burned': random.randint(200, 600),
                    'active_minutes': random.randint(30, 120),
                }
            )

        self.stdout.write(self.style.SUCCESS('Created 14 days of activity logs'))
        self.stdout.write(self.style.SUCCESS(
            '\n✅ Sample data loaded successfully!\n'
            '   Login credentials:\n'
            '   Username: john_fitness\n'
            '   Password: FitTrack123!\n'
        ))