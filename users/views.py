from unicodedata import category
from pymysql import NULL
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ValidationError
#from .serializers import UserSerializer, ChangePasswordSerializer, UpdateUserSerializer,EmailVerificationSerializer
from .serializers import UserSerializer, ChangePasswordSerializer, RequestPasswordResetEmailSerializer, SetNewPasswordSerializer, UpdateUserSerializer, DeactivateAccountSerializer
from .models import *
from .serializers import *
from .utils import Util
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.urls import reverse
import jwt, datetime
from django.http import HttpResponsePermanentRedirect,HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework import status,generics
from django.http import HttpResponse
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics,status,views
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
import os
from django.contrib.auth.models import Group


   
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
                email_body = 'Hi There '+ user.name +' \n Use the link below to verify your email \n' + absurl
                to_email= user.email
               # print(to_email)
                data = {'email_body': email_body, 'to_email': to_email ,'email_subject': 'Verify your email'}
        
                Util.send_email(data)
                user.role.add(Role.objects.get(Type="simple user"))

                return HttpResponseRedirect(redirect_to='https://google.com')

                #return Response(user_data)


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
       # if user.is_verified:

        if user is None:
                    raise AuthenticationFailed('User not found!')
        if not user.check_password(password):
                raise AuthenticationFailed('Incorrect password!')
            
        if not user.is_active:
                raise AuthenticationFailed('your acount is disabled!')

        payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
            #token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
                'jwt': token
            }
        return response
       # else:
            #return Response({"detail":"Go and confirm your email"},status=status.HTTP_400_BAD_REQUEST)
    

class UserView(APIView):
    
    def get(self, request):
        
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')   
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated! expired token ')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        print()
        return Response(serializer.data)
    

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class ChangePasswordView(generics.UpdateAPIView):
    
    queryset = User.objects.all()
  #  permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer    
    def get_object(self):
        token = self.request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!, expired token')
        user = User.objects.filter(id=payload['id']).first()
        return user
    


class UpdateProfileView(generics.UpdateAPIView):
    
    queryset = User.objects.all()
  #  permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer 
    
    def get_object(self):
        token = self.request.COOKIES.get('jwt')
        
        if not token:

            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!, expired token')

        user = User.objects.filter(id=payload['id']).first()
        return user
    
    
    def update(self, request, *args, **kwargs):
        if "email" in request.data :
            return Response({"detail" :"You are not allowed to change the email"}, status=status.HTTP_403_FORBIDDEN)
        return super(UpdateProfileView, self).update(request, *args, **kwargs)
    


#ResetPassword
class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = ['http', 'https']


class RequestPasswordResetEmailView(generics.GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        return Response({"detail" :"No user found "}, status=status.HTTP_400_BAD_REQUEST)
        


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')
                    
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class Deactivate_account(generics.CreateAPIView):
    queryset = User.objects.all()

    serializer_class = DeactivateAccountSerializer
    def get_object(self):
        token = self.request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!, expired token')

        user = User.objects.filter(id=payload['id']).first()
        return user
        
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        password=request.data.get("password",None)
        if password:
            user=self.get_object()
            if user.check_password(password):
                user.is_active = False
                user.save()
                return Response({ 'success':True,'message': 'Profile successfully disabled!'}, status=status.HTTP_200_OK)
            else:
                return Response({" detail":"Password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({ 'success':False,'message': 'A password is required to deactivate your account'}, status=status.HTTP_400_BAD_REQUEST)

class RoleView(generics.ListCreateAPIView):
        serializer_class=roleSerializer
        def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            return Role.objects.all()
        
        def post(self, request, *args, **kwargs):
            if request.data["Type"]=="chef service":
                request.data['category'] =  Category.objects.only('id').get(title=request.data['category'])
                if Role.objects.filter(category=request.data['category']).exists():
                    raise IntegrityError("role already exists!")
                else:
                    return self.create(request, *args, **kwargs)

            else:
                if Role.objects.filter(Type=request.data['Type']).exists():
                    raise IntegrityError("role already exists!")
                else:
                    request.data['category']=None
                    return self.create(request, *args, **kwargs)

           # return Response({"detail":"role added successfully"},status=status.HTTP_200_OK)
class DeleteRoleView(generics.DestroyAPIView):
    serializer_class=roleSerializer

    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            return Role.objects.all()


class RoleAssignmentView(generics.CreateAPIView):
    serializer_class=roleuUerSerializer
    queryset=Role.objects.all()
    def post(self, request, *args, **kwargs):
        token = self.request.COOKIES.get('jwt')
        
        if not token:
                raise AuthenticationFailed('Unauthenticated!')

        try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated!, expired token')
        if request.data["Type"]=="chef service":
            request.data['category'] =  Category.objects.only('id').get(title=request.data['category'])
            if Role.objects.filter(category=request.data['category']).exists():
                user=User.objects.get(id=request.data["user"])
                user.role.add(Role.objects.get(category=request.data['category']))
                return Response({"detail":"user assigned successfully"},status=status.HTTP_200_OK)
            else:
                raise IntegrityError("role does not exist!")
        else:
            if Role.objects.filter(Type=request.data['Type']).exists():
                user=User.objects.get(id=request.data["user"])
                user.role.add(Role.objects.get(Type=request.data['Type']))
                return Response({"detail":"user assigned successfully"},status=status.HTTP_200_OK)
            else:
                raise IntegrityError("role does not exist!")

class UnassignRoleView(generics.GenericAPIView):
        serializer_class=roleuUerSerializer
        
        def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            return Role.objects.all()
        def post(self, request,   *args, **kwargs):
            try:
                instance=self.get_object()
                user=User.objects.get(id=request.data["user"])
                user.role.remove(instance)
                return Response({"detail":"role unassigned successfully"}, status=status.HTTP_200_OK)
            except:
                return Response({"detail":"error"}, status=status.HTTP_400_BAD_REQUEST)  
    







    
