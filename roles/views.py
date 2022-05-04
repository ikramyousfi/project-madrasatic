import sys
sys.path.append("..") # Adds higher directory to python modules path.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import RoleSerializer
#from ..users.models import User
from .models import Role
import jwt, datetime

# Create your views here.

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
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)