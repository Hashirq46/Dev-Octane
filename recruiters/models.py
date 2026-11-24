from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from parsing.storage import private_storage

ntn_validator = RegexValidator(
    r'^\d{7}-?\d?$|^\d{13}$',
    'Enter NTN like 1234567-8 (or 13-digit CNIC for individuals).'
)
cuin_validator = RegexValidator(r'^\d{7}$', 'CUIN must be 7 digits.')


class ActiveTaxpayer(models.Model):
    """Local copy of FBR's downloadable Active Taxpayer List."""
    ntn = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=300)
    imported_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ntn} - {self.name}"


class RecruiterVerification(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending'
        APPROVED = 'approved'
        REJECTED = 'rejected'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=300)
    ntn = models.CharField(max_length=20, validators=[ntn_validator])
    cuin = models.CharField(max_length=7, blank=True, validators=[cuin_validator])  # blank for sole proprietors
    address = models.CharField(max_length=400, blank=True)
    city = models.CharField(max_length=80, blank=True)
    ntn_cert = models.FileField(upload_to='verification/ntn/', storage=private_storage)
    incorporation_cert = models.FileField(upload_to='verification/secp/', storage=private_storage, blank=True)
    ntn_on_atl = models.BooleanField(default=False)
    flags = models.JSONField(default=list, blank=True)  # automatic warnings for the admin
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    reviewer_note = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old = RecruiterVerification.objects.filter(pk=self.pk).values('company_name', 'ntn', 'cuin', 'status').first()
            if old and old['status'] == self.Status.APPROVED:
                if (old['company_name'] != self.company_name or 
                    old['ntn'] != self.ntn or 
                    old['cuin'] != self.cuin):
                    self.status = self.Status.PENDING
                    self.reviewed_by = None
                    self.reviewed_at = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.company_name} ({self.status})"
