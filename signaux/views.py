from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import SignalSerializer
from users.serializers import UserSerializer
from rest_framework import generics
from .models import Signal,Categorie
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
            signal = request.data 
            token = request.COOKIES.get('jwt')
        
           # cat = Categorie.objects.get(id=5)
            #print(cat.id)
            
            if not token:
                raise AuthenticationFailed('Unauthenticated! you cant send a signal, try to log in ')   
            try:
                payload = jwt.decode(token, 'secret', algorithm=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated! you cant send a signal, try to log in ')
            
            #user = User.objects.filter(id=payload['id']).first()
            #print(payload["id"])
            
            new_signal=Signal.objects.create(titre=signal["titre"],description=signal["description"],categorie=signal["categorie"],lieu=signal["lieu"],picture=signal["picture"], user_id=payload["id"])        
            new_signal.save()
            #print('hhhhhhhdddddddddddddddhh')
            #print(new_signal.titre)
            serializer = SignalSerializer(new_signal)
            return Response(serializer.data)
        
       

    
    
            
        
    
