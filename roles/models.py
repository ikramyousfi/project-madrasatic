from django.db import models

# Create your models here.
class Role(models.Model):
    RoleID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True)
    RoleName = models.CharField(max_length=32, unique=True, null=False , blank=False)
    CreateAccount       = models.BooleanField(default=False,)
    DesactivateAccount  = models.BooleanField(default=False, null=False)
    DeleteAccount       = models.BooleanField(default=False, null=False)
    ActivateAccount     = models.BooleanField(default=False, null=False)
    Addrole             = models.BooleanField(default=False, null=False)
    Editrole            = models.BooleanField(default=False, null=False)
    Deleterole          = models.BooleanField(default=False, null=False)
    EditCategory        = models.BooleanField(default=False, null=False)
    DeleteCategory      = models.BooleanField(default=False, null=False)
    AddCategory         = models.BooleanField(default=False, null=False)