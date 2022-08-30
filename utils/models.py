from django.db import models


class BaseModel(models.Model):
    """ Base model for other classes. """

    created_at = models.DateTimeField(
        'Created at',
        auto_now_add=True,
        help_text='Date time on which the object was created.'
        )

    updated_at = models.DateTimeField(
        'Last modified at',
        auto_now_add=True,
        help_text='Date time of the last time the object was modified.'
    )

    class Meta:
        """Meta option."""

        abstract = True

        get_latest_by = 'created_at'
        ordering = ['-created_at', '-updated_at']
