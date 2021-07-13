from django.db import models
from django.utils.timezone import now

from apps.decks.models import Deck
from apps.utils.models import Timestamps

class Card(Timestamps):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    bucket = {
        (1, '1 day'),
        (2, '3 days'),
        (3, '7 days'),
        (4, '16 days'),
        (5, '30 days'),
    }
    bucket = models.IntegerField(choices=bucket, default=1)
    next_review_at = models.DateTimeField(default=now)
    last_review_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.question