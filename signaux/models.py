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
        ('accepted', 'accepted'),
        ('treated','treated')
        
    ]
    #categories = [
       # ('hygiene', 'hygiene'),
       # ('materiel', 'materiel'),
       # ('electrecite', 'electrecite'),
        
   # ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Signal")
    picture = models.ImageField(blank=True, null=True, upload_to='./pics')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255,blank=True, null=True)
    #category = models.CharField(max_length=255,choices=categories,default='hygiene',)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,related_name="Signal") 
    place= models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255,choices=status,default='pending',)
  #  category = models.ForeignKey(Categorie, on_delete=models.CASCADE, default=1)
    
    
    

