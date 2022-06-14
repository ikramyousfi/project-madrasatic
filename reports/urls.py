from django.urls import path

from .views import ApprovedReportListView, ListReport, RejectedReportListView, ReportDetail, RequestChangeReportListView, ToBeApprovedReportListView, ToBeApprovedReportsUpdateView,UpdateReportView
urlpatterns =[
    path('ListReport',ListReport.as_view()),
    path('Update_Report/<pk>',UpdateReportView.as_view()),
    path('Update_Report_Status/<pk>',ToBeApprovedReportsUpdateView.as_view()),
    path('Report/<pk>',ReportDetail.as_view()),
    path('Pending_reports',ToBeApprovedReportListView.as_view()),
    path('Rejected_reports', RejectedReportListView.as_view()),
    path('Approved_reports', ApprovedReportListView.as_view()),
    path('Request_change_reports', RequestChangeReportListView.as_view()),
]