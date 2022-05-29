from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import DeclarationSerializer,CategorySerializer
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

    

    
#class displayCategorie(APIView):       
 #  def get(self, title):
  #      title="materiel"
   #     cat = Categorie.objects.get(titre=title)
        
    #    data = {'id':cat.id, 'titre': cat.titre, 'description': cat.description}
     #   return Response(data)    
    
class ListDeaclaration(generics.ListCreateAPIView):
    serializer_class = DeclarationSerializer
    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            return Declaration.objects.all()


    def post(self, request,*args,**kwargs):
            self.get_queryset()
            token = self.request.COOKIES.get('jwt')
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])   
            user_id=payload['id']
            request.data.update({"user":user_id})
            serializer=self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    
    


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
        def post(self, request, *args, **kwargs):
            self.get_queryset()
            return super().post(request, *args, **kwargs)
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

    

        
            
        
    
