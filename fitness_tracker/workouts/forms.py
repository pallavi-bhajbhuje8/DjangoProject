from django import forms
from .models import Workout


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['workout_type', 'duration', 'distance', 'calories_burned',
                  'intensity', 'date', 'start_time', 'notes']
        widgets = {
            'workout_type': forms.Select(attrs={'class': 'form-select'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': '1',
                                                  'placeholder': 'Minutes'}),
            'distance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01',
                                                  'placeholder': 'km (optional)'}),
            'calories_burned': forms.NumberInput(attrs={'class': 'form-control', 'min': '0',
                                                        'placeholder': 'Calories'}),
            'intensity': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                            'placeholder': 'Any notes about your workout...'}),
        }