from rest_framework import serializers
from .models import Category, Signal

class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signal
        fields = ['title', 'description', 'category', 'place', 'picture','user']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields="__all__"
