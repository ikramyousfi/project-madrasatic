
from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from signaux.models import Category

class UserSerializer(serializers.ModelSerializer):
    password = serializers
    class Meta:
        model = User
<<<<<<< HEAD
        fields =  ['id', 'name', 'email', 'password'] 
=======
        fields = ['first_name','name', 'email','password', 'username', 'last_name','role','id']
>>>>>>> 5e0ce5c03ecea39e5e56b12921703152fb47de69
        extra_kwargs = { 
            'password': {'write_only': True}
        }
        

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance  
    def to_representation(self, instance):
        rep = super(UserSerializer, self).to_representation(instance)
        rep['role'] = [role.Type for role in instance.role.all()]
        return rep


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token ']         
    
     
#UpdatePassword
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)
    
   
    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')
    
    

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        token = self.context['request'].COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('token expired')
        user = User.objects.filter(id=payload['id']).first()
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


#UpdateUserProfile
class UpdateUserSerializer(serializers.ModelSerializer):
    ''' email = serializers.EmailField(required=True)'''
    
    class Meta:
        model = User
        fields = "__all__" #('username', 'name', 'last_name')
        read_only_fields=['email','id','password','is_staff','is_verified','is_active']

    ''' def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value 

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()

        return instance '''

#ResetPassword
class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True,  required= True)
    
    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        model = User
        fields = ['email','']
        

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    password2 = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64', 'password2']

        
    def validate(self, attrs):
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError({"password": "Password fields didn't match."})
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        #return super().validate(attrs)



class DeactivateAccountSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True, required=True)
    class Meta:
        model = User
        fields = ['password']
        

class roleSerializer(serializers.ModelSerializer):
    category=serializers.StringRelatedField()
    class Meta:
<<<<<<< HEAD
        model = role
        fields = '__all__'
        
# class servicesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = services
#         fields = '__all__' 
=======
        model = Role
        fields = ['Type','category']
  
    def to_internal_value(self, data):
      try:
        if data['Type']=='chef service':
           data['category'] =  Category.objects.only('id').get(title=data['category'])
        return data
      except Category.DoesNotExist:
          raise IntegrityError("Category does not exist")

class roleuUerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Role
        fields=['Type','user','category']
    def to_internal_value(self, data):
         try:
           data['user'] =  [User.objects.get(id=data['user'])]  
           return data
         except User.DoesNotExist:
           raise IntegrityError("User does not exist")
>>>>>>> 5e0ce5c03ecea39e5e56b12921703152fb47de69
