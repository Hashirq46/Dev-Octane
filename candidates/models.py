from django.conf import settings
from django.db import models
from parsing.storage import private_storage


class CandidateProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='candidate_profile'
    )
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=80, blank=True)
    headline = models.CharField(max_length=150, blank=True)
    skills = models.CharField(max_length=500, blank=True)  # comma separated
    experience_years = models.PositiveSmallIntegerField(default=0)
    resume = models.FileField(upload_to='resumes/', storage=private_storage, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name or self.user.email

    @property
    def completeness_percentage(self):
        fields = [self.full_name, self.phone, self.city, self.headline, self.skills, self.resume]
        filled = sum(1 for f in fields if f)
        has_edu = self.education.exists()
        has_exp = self.experience.exists()
        total = len(fields) + 2
        filled_total = filled + (1 if has_edu else 0) + (1 if has_exp else 0)
        return int((filled_total / total) * 100)


class Education(models.Model):
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=150, blank=True)
    institute = models.CharField(max_length=200, blank=True)
    year = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.degree} - {self.institute}"


class WorkExperience(models.Model):
    profile = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='experience')
    title = models.CharField(max_length=150, blank=True)
    company = models.CharField(max_length=200, blank=True)
    start = models.CharField(max_length=20, blank=True)
    end = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} at {self.company}"
