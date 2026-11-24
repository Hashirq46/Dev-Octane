from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_recruiter = models.BooleanField(default=False)
    is_candidate = models.BooleanField(default=False)

    @property
    def is_verified_recruiter(self):
        v = getattr(self, 'recruiterverification', None)
        return bool(v and v.status == 'approved')
