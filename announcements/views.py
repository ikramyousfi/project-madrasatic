from django.shortcuts import render

# Create your views here.
from unittest import installHandler
from django.shortcuts import render
from .serializers import AnnouncementSerializer,AnnouncementStatusSerializer,AnnouncementRequestForChangeSerializer
from .models import AnnouncementRequestForChange, User, Announcement
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.db.models import Q




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
            return Announcement.objects.filter(created_by=user_id).all()

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
            request.data.update({"created_by":user_id})
            request.data.update()
            serializer=self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Service agent or club can update the announcementonly if it's requested for change 
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
        return Announcement.objects.filter(created_by=user_id).all()

    serializer_class = AnnouncementSerializer
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance.status)
        if instance.status=='request_change':
            
            announcement_status='pending'
            request.data.update({"status":announcement_status})
            AnnouncementRequestForChange.objects.filter(declaration=instance.id).update(checked=True)
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
            return Announcement.objects.filter(status="request_change").all()

#Service agent or club  can delete a declaration he created when it's draft or pending

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
            return Announcement.objects.filter(  Q(created_by=user_id,status="draft") or Q(created_by=user_id,status="pending"))