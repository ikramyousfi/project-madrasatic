from pkg_resources import require
from rest_framework import serializers
from .models import Category, Declaration, RequestForChange
from rest_framework.exceptions import AuthenticationFailed
import jwt
from users.models import User



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields="__all__"

class RequestForChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestForChange
        fields = "__all__"
class SubDeclarationSerializer(serializers.ModelSerializer):
    change_requests = RequestForChangeSerializer(many=True, required=False)
    category = serializers.StringRelatedField()
    class Meta:
        model = Declaration
        fields = '__all__'
        #read_only_fields=['status']
    def to_representation(self, instance):
        rep = super(DeclarationSerializer, self).to_representation(instance)
        rep['category'] = instance.category.title
        return rep
    def to_internal_value(self, data):
      try:
        data['user'] = User.objects.get(id=data['user'])
        data['category'] =  Category.objects.only('id').get(title=data['category'])
        return data 
      except:
          raise Category.DoesNotExist("Category does not exist")
          

class DeclarationSerializer(serializers.ModelSerializer):
    change_requests = RequestForChangeSerializer(many=True, required=False)
    category = serializers.StringRelatedField()
    attached_declarations=SubDeclarationSerializer(many=True,required=False)
    class Meta:
        model = Declaration
        fields = '__all__'
        #read_only_fields=['status']
    def to_representation(self, instance):
        rep = super(DeclarationSerializer, self).to_representation(instance)
        rep['category'] = instance.category.title
        return rep
    def to_internal_value(self, data):
      try:
        data['user'] = User.objects.get(id=data['user'])
        data['category'] =  Category.objects.only('id').get(title=data['category'])
        return data 
      except:
          raise Category.DoesNotExist("Category does not exist")
          
class DeclarationStatusSerializer(serializers.ModelSerializer):
    change_requests = RequestForChangeSerializer(many=True, required=False)
   # change_requests_list = validated_data.pop("change_requests", None)

    def update(self, instance, validated_data):
        change_requests_list = validated_data.pop("change_requests", None)
        responsable=self.context['request'].data['responsable']
        responsable=User.objects.get(id=responsable)


        if change_requests_list:
            for change_request in change_requests_list:
                RequestForChange.objects.create(declaration=instance, **change_request, responsable=responsable)
        instance.status = validated_data["status"]
        
        instance.save()
        return instance

    class Meta:
        model = Declaration
        fields='__all__'
        read_only_fields=['title','category','user','picture','description','place']