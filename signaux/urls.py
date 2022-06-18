from django.urls import path
from .views import DeleteUserDeclaration, ListDeclaration , CategoriesList, CategoryDetailView, DeclarationDetail, ServiceDeclarationList,ToBeApprovedUpdateView,ToBeApprovedListView,RejectedListView,ApprovedListView,TreatedListView,RequestedChangeListView,ListDrafts,UpdateDeclarationView,AttachDeclarationView,DeattachDeclarationView
urlpatterns = [
    path('ListDeclaration', ListDeclaration.as_view()),
    path('ListCategory', CategoriesList.as_view()),   
    path('Category/<pk>', CategoryDetailView.as_view()),
    path('Declaration/<pk>', DeclarationDetail.as_view()),
    path('Update_status/<pk>', ToBeApprovedUpdateView.as_view()),
    path('Pending_declarations', ToBeApprovedListView.as_view()),
    path('Rejected_declarations', RejectedListView.as_view()),
    path('Approved_declarations', ApprovedListView.as_view()),
    path('Treated_declarations', TreatedListView.as_view()),
    path('Requested_change_declarations', RequestedChangeListView.as_view()),
    path('drafts', ListDrafts.as_view()),
    path('Update_declaration/<pk>', UpdateDeclarationView.as_view()),
    path('Attachdeclaration/<pk>', AttachDeclarationView.as_view()),
    path('Deattachdeclaration/<pk>', DeattachDeclarationView.as_view()),
    path('Delete_declaration/<pk>', DeleteUserDeclaration.as_view()),
    path('service_declaration', ServiceDeclarationList.as_view()),



]



