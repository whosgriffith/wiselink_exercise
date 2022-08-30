from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models

from utils.models import BaseModel


class Account(BaseModel, AbstractUser):
    organization_name = models.CharField(blank=True, null=True, max_length=255)
