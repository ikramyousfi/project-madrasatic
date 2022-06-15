from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import DeclarationSerializer,CategorySerializer,DeclarationStatusSerializer,BaseDeclarationSerializer
from users.serializers import UserSerializer
from rest_framework import generics
from .models import Declaration  , Category, RequestForChange
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
from django.db.models import Q
# Create your views here.
class ListDeclaration(generics.ListCreateAPIView):
    serializer_class = DeclarationSerializer

    #user can see his own declarations
    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            user_id=payload['id']
            return Declaration.objects.filter(user=user_id)

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
            declaration_status="pending"

            request.data.update({"user":user_id})
            request.data.update({"status":declaration_status})
            request.data.update()
            serializer=self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class DeclarationDetail(generics.RetrieveAPIView):
    serializer_class = DeclarationSerializer
    #details about a specific declaration, everyone can see the detials of an approved declaration
    def get_queryset(self):
        
        token = self.request.COOKIES.get('jwt')
            
        if not token:
                raise AuthenticationFailed('Unauthenticated!')

        try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated!, expired token')
        return Declaration.objects.filter(status="approved")   

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
        
        return Declaration.objects.filter(status="pending")
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
                instance=self.get_object()
                if request.data["status"]=="treated":
                        instance.attached_declarations.update(status="treated")

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
            return Declaration.objects.filter(status="pending",attached_to=None)


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
            return Declaration.objects.filter(status="rejected",attached_to=None)
   
            
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
            return Declaration.objects.filter(status="approved",attached_to=None)

#List all treated declarations
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
            return Declaration.objects.filter(status="treated",attached_to=None)

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
            return Declaration.objects.filter(status="request_change") 


class ListDrafts(generics.ListCreateAPIView):
    serializer_class = DeclarationSerializer

    #user can get a list of the declarations that are drafts
    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            user_id=payload['id']
            return Declaration.objects.filter(user=user_id,status='draft')

    #user can create a declaration and it stays as drafts 
    def post(self, request,*args,**kwargs):
            token = self.request.COOKIES.get('jwt')
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            user_id=payload['id']
            request.data.update({"user":user_id})

            serializer=self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#user can update his declaration only if it's draft or change request 
class UpdateDeclarationView(generics.UpdateAPIView):
    def get_queryset(self):
        token = self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!, expired token')
        user_id=payload['id']
        return Declaration.objects.filter(user=user_id)

    serializer_class = DeclarationSerializer
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance.status)
        if instance.status=='draft':
            print("reached draft if")
            serializer=self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return super(UpdateDeclarationView,self).update(request, *args, **kwargs)
        elif instance.status=='request_change':
            print(RequestForChange.objects.filter(declaration=instance.id))
            print("reached change_request if")
            declaration_status='pending'
            request.data.update({"status":declaration_status})
            RequestForChange.objects.filter(declaration=instance.id).update(checked=True)
            serializer=self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return super(UpdateDeclarationView,self).update(request, *args, **kwargs)
        else:
            return Response({"detail":"you are not allowed to modify your declaration"}, status=status.HTTP_400_BAD_REQUEST)

        



#List of declaration for each service Service
#not implemented yet i need to figure out a way to link between the category and its service 
class ServiceDeclarationList(generics.ListAPIView):
    serializer_class = DeclarationSerializer

    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            user_id=payload['id']
            return Declaration.objects.filter(user=user_id)

#attaching declaration
class AttachDeclarationView(generics.UpdateAPIView):
    serializer_class =BaseDeclarationSerializer
    def get_queryset(self):
         
        token = self.request.COOKIES.get('jwt')
                    
        if not token:
                        raise AuthenticationFailed('Unauthenticated!')

        try:
                        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
                        raise AuthenticationFailed('Unauthenticated!, expired token')
        return Declaration.objects.filter(attached_to=None)
    
    def update(self, request, *args, **kwargs):
                instance=self.get_object()
                print(instance.id)
                print(type(int(request.data["attached_to"])))
                print(type(instance.id))

                if int(request.data["attached_to"]) !=instance.id:
                        return super().update(request, *args, **kwargs) 

                else:
                        return Response({"detail":"You are trying to attach the declaration to itself"}, status=status.HTTP_400_BAD_REQUEST)  


            
#Deattach Declaration
class DeattachDeclarationView(generics.GenericAPIView):
    serializer_class =BaseDeclarationSerializer
    def get_queryset(self):
        token = self.request.COOKIES.get('jwt')
        if not token:
                        raise AuthenticationFailed('Unauthenticated!')
        try:
                        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
                        raise AuthenticationFailed('Unauthenticated!, expired token')
        return Declaration.objects.all()
    def post(self, request,   *args, **kwargs):
        try:
                declaration=self.get_object()
                org_declaration=declaration.attached_to
                org_declaration.attached_declarations.remove(declaration)
                declaration.attached_to=None
                print(org_declaration)
                return Response({"detail":"success"}, status=status.HTTP_200_OK)
        except:
                return Response({"detail":"error"}, status=status.HTTP_400_BAD_REQUEST)  
    

#User can delete a declaration he created when it's draft or pending
class DeleteUserDeclaration(generics.DestroyAPIView):
    serializer_class = DeclarationSerializer

    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            user_id=payload['id']
            return Declaration.objects.filter(  Q(user=user_id,status="draft") or Q(user=user_id,status="pending"))