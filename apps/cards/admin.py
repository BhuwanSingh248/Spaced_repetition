from django.contrib import admin
from .models import Card
# print("============================")
class cardsAdmin(admin.ModelAdmin):
    list_display = (
        'deck',
        'question',
        'bucket'
    )

admin.site.register(Card, cardsAdmin)