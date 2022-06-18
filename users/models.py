from statistics import mode
from django.db import IntegrityError, models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin, Group)
from django.forms import model_to_dict
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group
# Create your models here.
class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None):
        if email is None:
            raise TypeError('Users should have a Email')
 
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user
        

    def create_superuser(self, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractUser):
    id= models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    picture = models.ImageField(blank=True, null=True, upload_to='./pics')
    is_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=20, unique=True, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    picture = models.ImageField(blank=True, null=True, upload_to='./pics')
    role= models.ManyToManyField('users.Role', related_name='user' ,blank=True,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    def __str__(self):
        return self.email
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        
       
        
class Role(models.Model):
    Type = models.CharField(max_length=255)
    category=models.OneToOneField('signaux.Category',on_delete=models.CASCADE,null=True,blank=True)
   # user=models.ForeignKey(User,on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
        return self.Type
 