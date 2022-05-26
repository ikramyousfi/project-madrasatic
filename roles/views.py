import sys
sys.path.append("..") # Adds higher directory to python modules path.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import  *
#from ..users.models import User
from .models import permissions
import jwt, datetime
from rest_framework import generics

# Create your views here.

ROLE_FORMAT = '''
{
    "RoleID": 1,
    "RoleName": "user",
    "CreateAccount": false,
    "DesactivateAccount": false,
    "DeleteAccount": false,
    "ActivateAccount": false,
    "Addrole": false,
    "Editrole": false,
    "Deleterole": false,
    "EditCategory": false,
    "DeleteCategory": false,
    "AddCategory": false
}
'''

class AddRole(APIView):
    
    def put(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        #user = User.objects.filter(id=payload['id']).first()
        #permission check
        serializer = permissionsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UpdateRoleView(generics.UpdateAPIView):
    
    queryset = permissions.objects.all()
  #  permission_classes = (IsAuthenticated,)
    serializer_class = UpdateRoleSerializer 
    
    def get_object(self):
        token = self.request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!, expired token')

        perm = permissions.objects.filter(RoleID=self.request.data['RoleID']).first()
        return perm
    def update(self, request, *args, **kwargs):
       
        return super(UpdateRoleView, self).update(request, *args, **kwargs)
