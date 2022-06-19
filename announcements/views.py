from django.shortcuts import render

# Create your views here.
from unittest import installHandler
from django.shortcuts import render
from .serializers import AnnouncementSerializer,AnnouncementStatusSerializer,AnnouncementRequestForChangeSerializer
from .models import AnnouncementRequestForChange, Announcement
from users.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.db.models import Q
from django.db import IntegrityError





# Create your views here.

#Service Agent or club can see the announcements he created and also create others
class ListAnnouncement(generics.ListCreateAPIView):
    serializer_class = AnnouncementSerializer
    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            user_id=payload['id']
            user= User.objects.get(id=user_id)
            user_roles_types = [role.Type for role in user.role.all()]
            print(user_roles_types)
            if "chef service"  in user_roles_types: 
                return Announcement.objects.filter(created_by=user_id)
            elif "club scientifique"  in user_roles_types:
                return Announcement.objects.filter(created_by=user_id)
            else:
                raise IntegrityError("only scientific clubs and chef services are allowed here")

    def post(self, request,*args,**kwargs):
            token = self.request.COOKIES.get('jwt')
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            user_id=payload['id']
            user= User.objects.get(id=user_id)
            user_roles_types = [role.Type for role in user.role.all()]
            print(user_roles_types)
            if ("chef service" not in user_roles_types) and ("club scientifique"  not in user_roles_types): 
                        raise IntegrityError("only scientific clubs and chef services are allowed here")
            else:
                request.data.update({"created_by":user_id})
                request.data.update()
                serializer=self.serializer_class(data=request.data)
                if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Service agent or club can update the announcementonly if it's requested for change or drafts
class UpdateAnnouncementView(generics.UpdateAPIView):
    def get_queryset(self):
        token = self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!, expired token')
        user_id=payload['id']
        user= User.objects.get(id=user_id)
        user_roles_types = [role.Type for role in user.role.all()]
        print(user_roles_types)
        if ("chef service" not in user_roles_types) and ("club scientifique"  not in user_roles_types): 
                        raise IntegrityError("only scientific clubs and chef services are allowed here")
        else:
                        return Announcement.objects.filter(created_by=user_id).all()

    serializer_class = AnnouncementSerializer
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance.status)
        if instance.status=='draft':
            serializer=self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return super(UpdateAnnouncementView,self).update(request, *args, **kwargs)
        elif instance.status=='request_change':
            
            announcement_status='pending'
            request.data.update({"status":announcement_status})
            AnnouncementRequestForChange.objects.filter(announcement=instance.id).update(checked=True)
            serializer=self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return super(UpdateAnnouncementView,self).update(request, *args, **kwargs)
        else:
            return Response({"detail":"you are not allowed to modify your declaration"}, status=status.HTTP_400_BAD_REQUEST)

#change announcements status
class ToBeApprovedAnnouncementsUpdateView(generics.UpdateAPIView):
    serializer_class = AnnouncementStatusSerializer
    def get_queryset(self):
        
        return Announcement.objects.filter(status="pending").all()
    def update(self, request, *args, **kwargs):
                
                token = self.request.COOKIES.get('jwt')
                    
                if not token:
                        raise AuthenticationFailed('Unauthenticated!')

                try:
                        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                except jwt.ExpiredSignatureError:
                        raise AuthenticationFailed('Unauthenticated!, expired token')
                user_id = payload['id']
                user= User.objects.get(id=user_id)
                user_roles_types = [role.Type for role in user.role.all()]
                print(user_roles_types)
                if "responsable" not in user_roles_types : 
                        raise IntegrityError("only responsibles are allowed here")
                else:
                        request.data.update({"responsable":user_id})
                        return super(ToBeApprovedAnnouncementsUpdateView, self).update(request, *args, **kwargs)

    #details about a specific announcement
class AnnouncementDetail(generics.RetrieveAPIView):
    serializer_class = AnnouncementSerializer
    def get_queryset(self):
        
        token = self.request.COOKIES.get('jwt')
            
        if not token:
                raise AuthenticationFailed('Unauthenticated!')

        try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated!, expired token')
        return Announcement.objects.filter(status="approved")

#List the Pending announcements for Responsible
class ToBeApprovedAnnouncementListView(generics.ListAPIView):
    
    serializer_class = AnnouncementSerializer
    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            user_id = payload['id']
            user= User.objects.get(id=user_id)
            user_roles_types = [role.Type for role in user.role.all()]
            print(user_roles_types)
            if "responsable" not in user_roles_types : 
                        raise IntegrityError("only responsibles are allowed here")
            else:
                        return Announcement.objects.filter(status="pending").all()

#List the Rejected Announcements for Responsible
class RejectedAnnouncementListView(generics.ListAPIView):
    
    serializer_class = AnnouncementSerializer
    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            user_id = payload['id']
            user= User.objects.get(id=user_id)
            user_roles_types = [role.Type for role in user.role.all()]
            print(user_roles_types)
            if "responsable" not in user_roles_types : 
                        raise IntegrityError("only responsibles are allowed here")
            else:
                        return Announcement.objects.filter(status="rejected").all()

#List the Approved Announcements for Responsible
class ApprovedAnnouncementListView(generics.ListAPIView):
    
    serializer_class = AnnouncementSerializer
    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            user_id = payload['id']
            user= User.objects.get(id=user_id)
            user_roles_types = [role.Type for role in user.role.all()]
            print(user_roles_types)
            if "responsable" not in user_roles_types : 
                        raise IntegrityError("only responsibles are allowed here")
            else:
                        return Announcement.objects.filter(status="approved").all()

#List the Change request announcements for Responsible
class RequestChangeAnnouncementListView(generics.ListAPIView):
    
    serializer_class = AnnouncementSerializer
    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            user_id = payload['id']
            user= User.objects.get(id=user_id)
            user_roles_types = [role.Type for role in user.role.all()]
            print(user_roles_types)
            if "responsable" not in user_roles_types : 
                        raise IntegrityError("only responsibles are allowed here")
            else:
                        return Announcement.objects.filter(status="request_change").all()


#Service agent or club  can delete an announcement when it's pending

class DeleteUserAnnouncement(generics.DestroyAPIView):  
    serializer_class = AnnouncementSerializer
    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            user_id=payload['id']
            user= User.objects.get(id=user_id)
            user_roles_types = [role.Type for role in user.role.all()]
            print(user_roles_types)
            if ("chef service" not in user_roles_types) and ("club scientifique"  not in user_roles_types): 
                        raise IntegrityError("only scientific clubs and chef services are allowed here")
            else:
                        return Announcement.objects.filter(  Q(created_by=user_id,status="draft") or Q(created_by=user_id,status="pending"))

class ListDrafts(generics.ListCreateAPIView):
    serializer_class = AnnouncementSerializer

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
            user= User.objects.get(id=user_id)
            user_roles_types = [role.Type for role in user.role.all()]
            print(user_roles_types)
            if ("chef service" not in user_roles_types) and ("club scientifique"  not in user_roles_types): 
                        raise IntegrityError("only scientific clubs and chef services are allowed here")
            else:
                return Announcement.objects.filter(created_by=user_id,status='draft')

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
            user= User.objects.get(id=user_id)
            user_roles_types = [role.Type for role in user.role.all()]
            print(user_roles_types)
            if ("chef service" not in user_roles_types) and ("club scientifique"  not in user_roles_types): 
                        raise IntegrityError("only scientific clubs and chef services are allowed here")
            else:
                request.data.update({"user":user_id})

                serializer=self.serializer_class(data=request.data)
                if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)