from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'category', 'job_type', 'city',
            'experience_required', 'salary_min', 'salary_max',
            'skills', 'description', 'expires_at'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Senior Backend Engineer'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Software Development, Marketing, Sales'}),
            'job_type': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Lahore, Karachi, Islamabad, Remote'}),
            'experience_required': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Years'}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'PKR per month (optional)'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'PKR per month (optional)'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, PostgreSQL, Celery'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Detailed job description, responsibilities, and requirements...'}),
            'expires_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
