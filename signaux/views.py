from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import DeclarationSerializer,CategorySerializer,DeclarationStatusSerializer
from users.serializers import UserSerializer
from rest_framework import generics
from .models import Declaration  , Category
from users.models import User
from rest_framework.response import Response
from django.contrib import messages
from django.contrib.auth import authenticate, login
import jwt
from django.contrib import auth
from django.conf import settings
from rest_framework import status
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpResponse

# Create your views here.
class ListDeaclaration(generics.ListCreateAPIView):
    serializer_class = DeclarationSerializer

    #user can see his own declaration
    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            user_id=payload['id']
            return Declaration.objects.filter(user=user_id).all()

    #user can create a declaration
    def post(self, request,*args,**kwargs):
            token = self.request.COOKIES.get('jwt')
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            user_id=payload['id']
            request.data.update({"responsable":user_id})
            serializer=self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class DeclarationDetail(generics.RetrieveDestroyAPIView):
    serializer_class = DeclarationSerializer
    #details about a specific declaration
    def get_queryset(self):
        
        token = self.request.COOKIES.get('jwt')
            
        if not token:
                raise AuthenticationFailed('Unauthenticated!')

        try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated!, expired token')
        return Declaration.objects.all()
    
    #delete a specific declaration : needs to be permit to the responsible only 


class CategoriesList(generics.ListCreateAPIView):

        serializer_class = CategorySerializer
        def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            return Category.objects.all()
        def post(self, request,*args,**kwargs):
            token = self.request.COOKIES.get('jwt')
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            user_id=payload['id']
            request.data.update({"created_by":user_id})
            serializer=self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #get the current categories
        #add another category, we need to override it in order to restrict it to the user 

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    def get_queryset(self):
        
        token = self.request.COOKIES.get('jwt')
            
        if not token:
                raise AuthenticationFailed('Unauthenticated!')

        try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated!, expired token')
        return Category.objects.all()

        #we need to override the put,patch and delete in order to restrict it to the user 

    
#change declarations status
class ToBeApprovedUpdateView(generics.UpdateAPIView):
    serializer_class = DeclarationStatusSerializer
    def get_queryset(self):
        
        return Declaration.objects.filter(status="pending").all()
    def update(self, request, *args, **kwargs):
                
                token = self.request.COOKIES.get('jwt')
                    
                if not token:
                        raise AuthenticationFailed('Unauthenticated!')

                try:
                        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                except jwt.ExpiredSignatureError:
                        raise AuthenticationFailed('Unauthenticated!, expired token')
                user_id = payload['id']
                request.data.update({"responsable":user_id})
                return super(ToBeApprovedUpdateView, self).update(request, *args, **kwargs)
    

#List the Pending declarations for Responsible
class ToBeApprovedListView(generics.ListAPIView):
    
    serializer_class = DeclarationSerializer
    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            return Declaration.objects.filter(status="pending").all()


#List the rejected declarations for responsible
class RejectedListView(generics.ListAPIView):
    
    serializer_class = DeclarationSerializer
    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            return Declaration.objects.filter(status="rejected").all()
   
            
#List all approved declarations
class ApprovedListView(generics.ListAPIView):
    
    serializer_class = DeclarationSerializer
    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            return Declaration.objects.filter(status="approved").all()

#List all approved declarations
class TreatedListView(generics.ListAPIView):
    
    serializer_class = DeclarationSerializer
    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            return Declaration.objects.filter(status="treated").all()

#List the requested for change declarations
class RequestedChangeListView(generics.ListAPIView):
    
    serializer_class = DeclarationSerializer
    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            return Declaration.objects.filter(status="request_change").all() 
