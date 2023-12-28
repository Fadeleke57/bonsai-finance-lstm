from rest_framework import serializers
from .models import lstmData

class lstmDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = lstmData
        fields = ['id', 'name', 'description']