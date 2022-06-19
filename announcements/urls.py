from django.urls import path
from announcements.views import AnnouncementDetail, ApprovedAnnouncementListView, DeleteUserAnnouncement, ListAnnouncement, RejectedAnnouncementListView, RequestChangeAnnouncementListView, ToBeApprovedAnnouncementListView, ToBeApprovedAnnouncementsUpdateView, UpdateAnnouncementView

urlpatterns =[
    path('ListAnnouncement',ListAnnouncement.as_view()),
    path('Update_Announcement/<pk>',UpdateAnnouncementView.as_view()),
    path('Update_Announcement_Status/<pk>',ToBeApprovedAnnouncementsUpdateView.as_view()),
    path('Announcement/<pk>',AnnouncementDetail.as_view()),
    path('Pending_announcements',ToBeApprovedAnnouncementListView.as_view()),
    path('Rejected_announcements', RejectedAnnouncementListView.as_view()),
    path('Approved_announcements', ApprovedAnnouncementListView.as_view()),
    path('Request_change_announcements', RequestChangeAnnouncementListView.as_view()),
        path('Delete_announcement/<pk>', DeleteUserAnnouncement.as_view()),

]