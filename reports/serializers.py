from pkg_resources import require
from rest_framework import serializers
from .models import  ReportRequestForChange,Report,User,Declaration
from rest_framework.exceptions import AuthenticationFailed
import jwt


class ReportRequestForChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportRequestForChange
        fields = "__all__"


class ReportSerializer(serializers.ModelSerializer):
    report_change_requests = ReportRequestForChangeSerializer(many=True, required=False)
    class Meta:
        model = Report
        fields="__all__"

class ReportStatusSerializer(serializers.ModelSerializer):
    report_change_requests = ReportRequestForChangeSerializer(many=True, required=False)
    def update(self, instance, validated_data):
        report_change_requests_list = validated_data.pop("report_change_requests", None)
        responsable=self.context['request'].data['responsable']
        responsable=User.objects.get(id=responsable)


        if report_change_requests_list:
            for change_request in report_change_requests_list:
                ReportRequestForChange.objects.create(report=instance, **change_request, responsable=responsable)
        instance.status = validated_data["status"]
        instance.save()
        return instance

    class Meta:
        model = Report
        fields='__all__'
        read_only_fields=['title','description','created_by','attached_file','declaration']