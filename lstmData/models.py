from django.db import models
from django.utils import timezone

# Create your models here.
"""
class lstmData(models.Model):
    stockSymbol = models.CharField(max_length=10, default='')  # e.g., 'AAPL'
    predictedPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    predictionDate = models.DateField(default=timezone.now)

    def __str__(self):
        return self.stockSymbol
"""