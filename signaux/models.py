from django.db import models
from users.models import User


# Create your models here.

class Categorie(models.Model):
      
  #picture = models.ImageField(blank=True, null=True, upload_to='./pics')
    titre = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    
    
class Signal(models.Model):
    status = [
        ('pending', 'pending'),
        ('rejected', 'rejected'),
        ('accepted', 'accepted'),
        
    ]
    categories = [
        ('hygiene', 'hygiene'),
        ('materiel', 'materiel'),
        ('electrecite', 'electrecite'),
        
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(blank=True, upload_to='./pics')
    titre = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    categorie = models.CharField(max_length=255,choices=categories,default='hygiene',)
    lieu = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255,choices=status,default='pending',)
  #  category = models.ForeignKey(Categorie, on_delete=models.CASCADE, default=1)
    
    
    

