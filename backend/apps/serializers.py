from rest_framework import serializers
from .models import PsychometricWeights

class PsychometricWeightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PsychometricWeights
        fields = ('weights')
