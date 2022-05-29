from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import SignalSerializer,CategorySerializer
from users.serializers import UserSerializer
from rest_framework import generics
from .models import Signal  , Category
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

    

    
#class displayCategorie(APIView):       
 #  def get(self, title):
  #      title="materiel"
   #     cat = Categorie.objects.get(titre=title)
        
    #    data = {'id':cat.id, 'titre': cat.titre, 'description': cat.description}
     #   return Response(data)    
    
class addSignal(generics.GenericAPIView):
    serializer_class = SignalSerializer
    
    def post(self, request,*args,**kwargs):
            token = request.COOKIES.get('jwt')
        
            
           # cat = Categorie.objects.get(id=5)
            #print(cat.id)
            
            if not token:
                raise AuthenticationFailed('Unauthenticated! you cant send a signal, try to log in ')   
            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated! you cant send a signal, try to log in ')
            
           
            #new_signal=Signal.objects.create( titre=signal["titre"],description=signal["description"],categorie=signal["categorie"],lieu=signal["lieu"],picture=signal["picture"], user_id=payload["id"])        
            #new_signal.save()
            #serializer = SignalSerializer(new_signal)
            #return Response(serializer.data)
            #print(payload['id'])  
            user_id=payload['id']
            request.data.update({"user":user_id})
            serializer=self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    
    


class CategoriesList(generics.ListCreateAPIView):
        queryset = Category.objects.all()
        serializer_class = CategorySerializer
        #get the current categories
        def get(self, request, *args, **kwargs) :
            token = request.COOKIES.get('jwt')
            if not token:
                raise AuthenticationFailed('Unauthenticated! , try to log in ')   
            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated! , try to log in ')
            #user_id=payload['id']
            return super(CategoriesList, self).get(request, *args, **kwargs)

        #add another category 
        def post(self, request, *args, **kwargs) :
            token = request.COOKIES.get('jwt')
            if not token:
                raise AuthenticationFailed('Unauthenticated! , try to log in ')   
            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated! , try to log in ')
            #user=payload['id']
            
            return super(CategoriesList, self).post(request, *args, **kwargs)
             #response({'message':'You are not allowed to make this action'}, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
        
    
    def get(self, request, *args, **kwargs):
        token = self.request.COOKIES.get('jwt')
            
        if not token:
                raise AuthenticationFailed('Unauthenticated!')

        try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated!, expired token')
        return super(CategoryDetailView, self).get(request, *args, **kwargs)

   

    def patch(self, request, *args, **kwargs):
        token = self.request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!, expired token')
        return super(CategoryDetailView, self).patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        token = self.request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!, expired token')
        return super(CategoryDetailView, self).delete(request, *args, **kwargs)
    
    

        
            
        
    
