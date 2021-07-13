from django.db import models

# Create your models here.
from apps.utils.models import Timestamps

class Deck(Timestamps):
    title = models.CharField(max_length=100)
    description = models.TextField()
    last_reviewed = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title