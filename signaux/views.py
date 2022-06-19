from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import DeclarationSerializer,CategorySerializer,DeclarationStatusSerializer
from users.serializers import UserSerializer
from rest_framework import generics
from rest_framework import viewsets
from .models import Declaration, Category
from users.models import User, role
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
from django.contrib.auth import get_user_model

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
           
           
        #     roe=role.objects.filter(id_user=user_id)
        #     print(roe)
           
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
            declaration_status="pending"
            request.data.update({"user":user_id})
            request.data.update({"status":declaration_status})
            
            serializer=self.serializer_class(data=request.data)
            

            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
   
   #display a declaration to responsable

        
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

def index(request):
    declarations = Declaration.objects.all()
    categories = Category.objects.all()
    val=0;
    x=[]
    y=[]
    print(categories)
    for categorie in categories :
        x.append(categorie.title)
        val=0
        for declaration in declarations :
                if declaration.category.id==categorie.id : 
                        val=val+1
                        
        y.append(val)
    print(x)
    print(y)   
        
    context = {
        "declarations": declarations,
        "categories":categories,
        "val":val,
        "x":x,
        "y":y,

        

    }

    return render(request, 'chartapp/index.html', context)
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
            return Declaration.objects.filter(user=user_id,status='draft').all()

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
    

# # class ChefServiceView(viewsets.ModelViewSet):
#     serializer_class = ChefServiceSerializer
#     queryset = ChefService.objects.all()

#     def create(self, request):
            
#         token = self.request.COOKIES.get('jwt')
#         payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         #user = User.objects.filter(id=payload['id']).first()
#         user=get_user_model().objects.filter(id=payload['id']).first()
#         print(user)
#         user=get_user_model().objects.filter(id=request.data['id_user']).first()
        
#         print(request.data['id_category'])
#         test_chef_service= user.groups.filter(name='Chef service').exists()
#         print(test_chef_service)
        
#         if not token:
#             raise AuthenticationFailed(' Unauthenticated!')   
#         try:
#             payload = jwt.decode(token, 'secret', algorithm=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Unauthenticated!')
        
#         if test_chef_service is True:
#                 return super().create(request)
#         if test_chef_service is False:
#                 return Response({"detail": 'role chef service does not exist'}, status=status.HTTP_200_OK)
                    