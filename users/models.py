from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models

from utils.models import BaseModel


class Account(BaseModel, AbstractUser):
    organization_name = models.CharField(blank=True, null=True, max_length=255)
    created_events = models.PositiveIntegerField(default=0)
    finished_events = models.PositiveIntegerField(default=0)
    cancelled_events = models.PositiveIntegerField(default=0)
    attended_events = models.PositiveIntegerField(default=0)
