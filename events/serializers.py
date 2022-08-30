from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from events.models import Event


class EventModelSerializer(serializers.ModelSerializer):
    organizer = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Event
        fields = ('organizer', 'title', 'short_description', 'long_description', 'date_time', 'location',
                  'status')
        read_only_fields = ('organizer', )

    def validate_date_time(self, data):
        valid_date = timezone.now() + timedelta(hours=2)
        if data < valid_date:
            raise serializers.ValidationError("Event can't be created less than 2 hours before starting.")
        return data


class UpdateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('title', 'short_description', 'long_description', 'date_time', 'location', 'status')
