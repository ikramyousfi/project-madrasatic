from django.db import models
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
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="reports")
    status = models.CharField(max_length=255,choices=status,default='pending')
    attached_file = models.FileField(upload_to='./reports',null=True, blank=True)
    declaration = models.ForeignKey('signaux.Declaration',on_delete=models.CASCADE,related_name="report")
    declaration_treated= models.BooleanField(default=False)
    #this is in case the treatement of a declaration will go through many phases, so it would have each time a report 
    #this attribute is set to true by the agent when he completes the whole treatement of the declaration 
    #so when the responsible approve the report , the status and its attached ones will be treated .

class ReportRequestForChange(models.Model):
  title = models.CharField(max_length=255, blank=True, null=True)
  comment = models.TextField(max_length=255, blank=True, null=True)
  checked = models.BooleanField(default=False)
  responsable = models.ForeignKey('users.User', on_delete=models.CASCADE , null=True, blank=True)
  report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="report_change_requests",   null=True, blank=True)

