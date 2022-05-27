
from django.db import models
import sys
sys.path.append('../')
from users.models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt



# Create your models here.
class permissions(models.Model):
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
    
    def get_user_perm(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        id = user.id
        roles = Role.objects.filter(UserID=id).all()
        #perms = permissions.

#  def perm_add_role(self, request):
        #id


class Role(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True)
    UserID = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    RoleID = models.ForeignKey(permissions, on_delete= models.CASCADE)

