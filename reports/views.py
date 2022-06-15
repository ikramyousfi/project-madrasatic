from unittest import installHandler
from django.shortcuts import render
from .serializers import ReportRequestForChangeSerializer,ReportSerializer,ReportStatusSerializer
from .models import Report, User, ReportRequestForChange, Declaration
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.db.models import Q




# Create your views here.

#Service Agent can see the reports he created and also create other reports
class ListReport(generics.ListCreateAPIView):
    serializer_class = ReportSerializer
    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            user_id=payload['id']
            return Report.objects.filter(created_by=user_id).all()

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


#Service agent can update the report only if it's requested for change 
class UpdateReportView(generics.UpdateAPIView):
    def get_queryset(self):
        token = self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!, expired token')
        user_id=payload['id']
        return Report.objects.filter(created_by=user_id).all()

    serializer_class = ReportSerializer
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance.status)
        if instance.status=='request_change':
            print(ReportRequestForChange.objects.filter(report=instance.id))
            print("reached change_request if")
            report_status='pending'
            request.data.update({"status":report_status})
            ReportRequestForChange.objects.filter(declaration=instance.id).update(checked=True)
            serializer=self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return super(UpdateReportView,self).update(request, *args, **kwargs)
        else:
            return Response({"detail":"you are not allowed to modify your declaration"}, status=status.HTTP_400_BAD_REQUEST)

#change reports status
class ToBeApprovedReportsUpdateView(generics.UpdateAPIView):
    serializer_class = ReportStatusSerializer
    def get_queryset(self):
        
        return Report.objects.filter(status="pending").all()
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
                report=self.get_object()
                print(report)
                if request.data["status"]=="approved":
                    if report.declaration_treated:
                        report.declaration.status='treated'
                        report.declaration.save()
                        report.declaration.attached_declarations.update(status='treated')
                return super(ToBeApprovedReportsUpdateView, self).update(request, *args, **kwargs)

    #details about a specific report
#only responsable and agent seervice
class ReportDetail(generics.RetrieveAPIView):
    serializer_class = ReportSerializer
    def get_queryset(self):
        
        token = self.request.COOKIES.get('jwt')
            
        if not token:
                raise AuthenticationFailed('Unauthenticated!')

        try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated!, expired token')
        return Report.objects.all()

#List the Pending Reports for Responsible
class ToBeApprovedReportListView(generics.ListAPIView):
    
    serializer_class = ReportSerializer
    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            return Report.objects.filter(status="pending").all()

#List the Rejected Reports for Responsible
class RejectedReportListView(generics.ListAPIView):
    
    serializer_class = ReportSerializer
    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            return Report.objects.filter(status="rejected").all()

#List the Approved Reports for Responsible
class ApprovedReportListView(generics.ListAPIView):
    
    serializer_class = ReportSerializer
    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            return Report.objects.filter(status="approved").all()

#List the Change request Reports for Responsible
class RequestChangeReportListView(generics.ListAPIView):
    
    serializer_class = ReportSerializer
    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            return Report.objects.filter(status="request_change").all()

#Service agent can delete a declaration he created when it's draft or pending

class DeleteUserReport(generics.DestroyAPIView):  
    serializer_class = ReportSerializer
    def get_queryset(self):
            token = self.request.COOKIES.get('jwt')
                
            if not token:
                    raise AuthenticationFailed('Unauthenticated!')

            try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                    raise AuthenticationFailed('Unauthenticated!, expired token')
            user_id=payload['id']
            return Report.objects.filter(  Q(created_by=user_id,status="draft") or Q(created_by=user_id,status="pending"))