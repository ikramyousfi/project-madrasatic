from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin, Group)

from rest_framework_simplejwt.tokens import RefreshToken
import encodings.idna
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
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    def __str__(self):
        return self.email
    
    @property
    def roles(self):
        return self.role_set.all()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    
    def has_module_perms(self, app_label):
        return True
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        
ROLE_CHOICES = (
    ('simple user', 'simple user'),
    ('chef service', 'chef service'),
    ('responsable', 'responsable'),
)        
        
class role(models.Model):
    id_role= models.AutoField(primary_key=True, editable=False)
    id_user= models.ForeignKey(User, on_delete=models.CASCADE)
    Type = models.CharField(max_length=255, choices=ROLE_CHOICES)
    
    def __str__(self):
        return self.get_Type_display() 
    
    def addRole(id_user,Type):
            group = Group.objects.get(name=Type)
            user=User.objects.get(id=id_user)
            if group not in user.groups.all():
                user.groups.add(group)
                return True
            else : return False
    
    
    def deleteRole(id_user,Type):
        group = Group.objects.get(name=Type)
        user = id_user
        group.user_set.remove(user)