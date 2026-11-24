from django.conf import settings
from django.db import models
from .storage import private_storage


class ParsedDraft(models.Model):
    class Kind(models.TextChoices):
        CV = 'cv'
        COMPANY = 'company'

    class State(models.TextChoices):
        PENDING = 'pending'
        READY = 'ready'
        FAILED = 'failed'
        SUBMITTED = 'submitted'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kind = models.CharField(max_length=10, choices=Kind.choices)
    label = models.CharField(max_length=10, blank=True)  # 'cv', 'ntn', 'secp'
    file = models.FileField(upload_to='drafts/', storage=private_storage)
    state = models.CharField(max_length=10, choices=State.choices, default=State.PENDING)
    data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Draft #{self.id} ({self.kind}:{self.label}) - {self.state}"
