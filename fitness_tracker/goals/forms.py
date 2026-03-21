from django import forms
from .models import Goal


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['goal_type', 'title', 'description', 'target_value',
                  'current_value', 'unit', 'start_date', 'end_date', 'status']
        widgets = {
            'goal_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'e.g., Run 50km this month'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'target_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'current_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'e.g., km, kg, steps'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }