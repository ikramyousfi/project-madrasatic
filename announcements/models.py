from django.db import models
# Create your models here.


class Announcement(models.Model):
    status = [
        ('pending', 'pending'),
        ('rejected', 'rejected'),
        ('approved', 'approved'),
        ('request_change','request_change'),
        
    ]
    title=models.CharField(max_length=255)
    description = models.CharField(max_length=255,null=True,blank=True)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="announcements")
    status = models.CharField(max_length=255,choices=status,default='pending')
    picture = models.FileField(upload_to='./announcements',null=True, blank=True)


class AnnouncementRequestForChange(models.Model):
  title = models.CharField(max_length=255, blank=True, null=True)
  comment = models.TextField(max_length=255, blank=True, null=True)
  checked = models.BooleanField(default=False)
  responsable = models.ForeignKey('users.User', on_delete=models.CASCADE , null=True, blank=True)
  announcement = models.ForeignKey('announcements.Announcement', on_delete=models.CASCADE, related_name="announcement_change_requests",   null=True, blank=True)
