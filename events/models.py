from django.db import models

from utils.models import BaseModel
from users.models import Account

EVENT_STATUS = [
    ('draft', 'draft'),
    ('active', 'active'),
    ('cancelled', 'cancelled'),
]


class Event(BaseModel):
    organizer = models.ForeignKey('users.Account', on_delete=models.CASCADE, blank=True, null=True,
                                  related_name='organizer')
    title = models.CharField(blank=False, max_length=255)
    short_description = models.CharField('short description', blank=True, max_length=255)
    long_description = models.CharField('long description', blank=True, max_length=255)
    date_time = models.DateTimeField(blank=True, null=True)
    location = models.CharField(blank=True, max_length=255, default='TBD')
    status = models.CharField(max_length=9, choices=EVENT_STATUS, default='draft')
    participants = models.ManyToManyField(Account, blank=True)
