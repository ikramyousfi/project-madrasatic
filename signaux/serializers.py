from rest_framework import serializers
from .models import Signal, Categorie

class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signal
        fields = ['titre', 'description', 'categorie', 'lieu', 'picture']
