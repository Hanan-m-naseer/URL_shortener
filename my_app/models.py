from django.db import models
from django.utils import timezone

# Create your models here.


class Link(models.Model):
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=16, unique=True, db_index=True)
    clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"

