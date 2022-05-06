from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ValidationError
from .serializers import UserSerializer, EmailVerificationSerializer
from .models import User
from .utils import Util
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.urls import reverse
import jwt, datetime
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import redirect
from rest_framework import status,generics
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings

   
class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer
    def post(self, request):
        user = request.data
        regular='@esi-sba.dz'
        if (len(user['email']) > 11 ):
            if(user['email'][-11:] == regular):
                serializer = self.serializer_class(data=user)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                user_data = serializer.data
                user = User.objects.get(email=user_data['email'])
                
                token = RefreshToken.for_user(user).access_token
                
                
                current_site = get_current_site(request).domain
                relativeLink = reverse('emailverify')
                
                absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
                email_body = 'Hi There'+user.name +' \n Use the link below to verify your email \n' + absurl
                to_email= user.email
               # print(to_email)
                data = {'email_body': email_body, 'to_email': to_email ,'email_subject': 'Verify your email'}
        
                Util.send_email(data)
            
                return Response(user_data)
            else: 
                raise AuthenticationFailed('EMAIL INVALID')
            
        else: 
            raise AuthenticationFailed('EMAIL INVALID')
            
        
        



class VerifyEmail(APIView):
    
    def get(self, request):
       #pass
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if  not user.is_verified:
               # print(user.is_verified, "ggggggg")
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
   

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        
        if user is None:
                raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response
    

class UserView(APIView):
    
    def get(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)



class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response