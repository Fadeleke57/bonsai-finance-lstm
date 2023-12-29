
"""
from rest_framework import serializers
from .models import lstmData

from .lstmModelDriver.driver import Driver
from .lstmModelDriver.config import Configurations

class lstmDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = lstmData
        fields = ['stockSymbol', 'predictedPrice', 'predictionDate']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            "status": "success",
            "data": {
                "stockSymbol": representation.get('stockSymbol', ''),
                "predictedPrice": representation.get('predictedPrice', 0),
                "predictionDate": representation.get('predictionDate', ''),
            },
            "message": f"Next day stock price prediction for {representation.get('stockSymbol', '')}."
    }
"""