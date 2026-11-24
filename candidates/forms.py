from django import forms
from accounts.validators import validate_upload
from .models import CandidateProfile


class CandidateReviewForm(forms.Form):
    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'})
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+92 300 1234567'})
    )
    city = forms.CharField(
        max_length=80,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lahore, Karachi, Islamabad...'})
    )
    headline = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Senior Python Developer | Django & React'})
    )
    skills = forms.CharField(
        max_length=500,
        required=False,
        help_text='Comma-separated skills (e.g. Python, Django, SQL, REST APIs)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, PostgreSQL, Docker'})
    )
    experience_years = forms.IntegerField(
        min_value=0,
        max_value=60,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


class EducationForm(forms.Form):
    degree = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'BS Computer Science'})
    )
    institute = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'University Name'})
    )
    year = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': '2019 - 2023'})
    )


class ExperienceForm(forms.Form):
    title = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Software Engineer'})
    )
    company = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Company Name'})
    )
    start = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Jan 2021'})
    )
    end = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Present'})
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 2, 'placeholder': 'Role highlights and responsibilities...'})
    )


class CandidateProfileEditForm(forms.ModelForm):
    new_cv = forms.FileField(
        required=False,
        validators=[validate_upload],
        label='Upload New CV (triggers re-parsing and review)',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.docx,.jpg,.jpeg,.png'})
    )

    class Meta:
        model = CandidateProfile
        fields = ['full_name', 'phone', 'city', 'headline', 'skills', 'experience_years']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            'skills': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
        }
