import re
from django.db import models


# Create your models here.

class Category(models.Model):
      
    title = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255,null=True,blank=True)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="categories")
    
    def __str__(self):
        return self.title

    
class Declaration(models.Model):
    status = [
        ('pending', 'pending'),
        ('rejected', 'rejected'),
        ('approved', 'approved'),
        ('treated','treated'),
        ('request_change','request_change'),
        ('draft','draft')
        
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="declarations")
    picture = models.ImageField(blank=True, null=True, upload_to='./declarations')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255,blank=True, null=True)
    category=models.ForeignKey('signaux.Category', on_delete=models.CASCADE,related_name="declarations") 
    place= models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255,choices=status,default='draft',)
    attached_to= models.ForeignKey('self',  on_delete=models.SET_NULL, related_name="attached_declarations",   default=None, null=True, blank=True)

class RequestForChange(models.Model):
  title = models.CharField(max_length=255, blank=True, null=True)
  comment = models.TextField(max_length=255, blank=True, null=True)
  checked = models.BooleanField(default=False)
  responsable = models.ForeignKey('users.User', on_delete=models.CASCADE , null=True, blank=True)
  declaration = models.ForeignKey('signaux.Declaration', on_delete=models.CASCADE, related_name="change_requests",   null=True, blank=True)

