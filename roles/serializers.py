from rest_framework import serializers
from .models import permissions

class permissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = permissions
        fields = "__all__"
       

class UpdateRoleSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = permissions
        fields = "__all__" 
        read_only_fields=['RoleID']