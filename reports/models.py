from turtle import title
from django.db import models
from users.models import User
from signaux.models import Declaration
# Create your models here.


class Report(models.Model):
    status = [
        ('pending', 'pending'),
        ('rejected', 'rejected'),
        ('approved', 'approved'),
        ('request_change','request_change'),
        
    ]
    title=models.CharField(max_length=255)
    description = models.CharField(max_length=255,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    status = models.CharField(max_length=255,choices=status,default='pending')
    attached_file = models.FileField(upload_to='./reports',null=True, blank=True)
    declaration = models.ForeignKey(Declaration,on_delete=models.CASCADE,related_name="report")


class ReportRequestForChange(models.Model):
  title = models.CharField(max_length=255, blank=True, null=True)
  comment = models.TextField(max_length=255, blank=True, null=True)
  checked = models.BooleanField(default=False)
  responsable = models.ForeignKey(User, on_delete=models.CASCADE , null=True, blank=True)
  report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="report_change_requests",   null=True, blank=True)

