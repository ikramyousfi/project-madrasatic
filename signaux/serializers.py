from rest_framework import serializers
from .models import Category, Declaration


class DeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Declaration
        fields = '__all__'
        read_only_fields=['status']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields="__all__"
