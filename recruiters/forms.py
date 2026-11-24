from django import forms
from accounts.validators import validate_upload
from .models import RecruiterVerification


class CompanyDocsForm(forms.Form):
    ntn_cert = forms.FileField(
        validators=[validate_upload],
        label='NTN Registration Certificate *',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.docx,.jpg,.jpeg,.png'})
    )
    secp_cert = forms.FileField(
        required=False,
        validators=[validate_upload],
        label='SECP Incorporation Certificate (Optional for Sole Proprietors)',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.docx,.jpg,.jpeg,.png'})
    )
    consent = forms.BooleanField(
        label='I agree that uploaded certificates will be processed automatically by an external AI service for verification autofill.',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class VerificationForm(forms.ModelForm):
    class Meta:
        model = RecruiterVerification
        fields = ['company_name', 'ntn', 'cuin', 'address', 'city']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Registered Company Name'}),
            'ntn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1234567-8 or 13-digit CNIC'}),
            'cuin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '7-digit CUIN (leave blank for sole proprietors)'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Official business address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        }
        help_texts = {
            'cuin': 'Corporate Universal Identification Number from SECP (7 digits). Optional for sole proprietors.',
            'ntn': 'National Tax Number or 13-digit CNIC for individual proprietors.',
        }
