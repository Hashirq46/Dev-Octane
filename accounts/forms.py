from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import User
from .validators import validate_office_email, validate_upload


class BaseSignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create password'}))
    role = None  # 'is_candidate' or 'is_recruiter'

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean_password(self):
        pw = self.cleaned_data['password']
        validate_password(pw)
        return pw

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.set_password(self.cleaned_data['password'])
        user.is_active = False  # activated after email confirmation
        setattr(user, self.role, True)
        if commit:
            user.save()
        return user


class CandidateSignupForm(BaseSignupForm):
    role = 'is_candidate'
    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'})
    )
    cv = forms.FileField(
        validators=[validate_upload],
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.docx,.jpg,.jpeg,.png'})
    )
    consent = forms.BooleanField(
        label='I agree that my CV will be processed automatically by an external AI service to fill my profile.',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class RecruiterSignupForm(BaseSignupForm):
    role = 'is_recruiter'
    email = forms.EmailField(
        validators=[validate_office_email],
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'hr@yourcompany.com'})
    )


class ResendConfirmationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your registered email'})
    )
