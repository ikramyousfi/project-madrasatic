import re
from django.db import models
from users.models import User


# Create your models here.

class Category(models.Model):
      
  #picture = models.ImageField(blank=True, null=True, upload_to='./pics')
    title = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Category")

    
class Declaration(models.Model):
    status = [
        ('pending', 'pending'),
        ('rejected', 'rejected'),
        ('approved', 'approved'),
        ('treated','treated'),
        ('request_change','request_change')
        
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Signal")
    picture = models.ImageField(blank=True, null=True, upload_to='./pics')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255,blank=True, null=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,related_name="Signal") 
    place= models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255,choices=status,default='pending',)
    

class RequestForChange(models.Model):
  title = models.CharField(max_length=255, blank=True, null=True)
  comment = models.TextField(max_length=255, blank=True, null=True)
  checked = models.BooleanField(default=False)
  responsable = models.ForeignKey(User, on_delete=models.CASCADE , null=True, blank=True)
  declaration = models.ForeignKey(Declaration, on_delete=models.CASCADE, related_name="change_requests",   null=True, blank=True)