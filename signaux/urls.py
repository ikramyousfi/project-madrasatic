from django.urls import path
from rest_framework import routers
from django.urls import include
from .views import *
from .views import ListDeclaration , CategoriesList, CategoryDetailView, DeclarationDetail,ToBeApprovedUpdateView,ToBeApprovedListView,RejectedListView,ApprovedListView,TreatedListView,RequestedChangeListView,ListDrafts
from . import views


router = routers.DefaultRouter()
# router.register(r'chefservice', ChefServiceView, basename='ChefService')


urlpatterns = [
    path('', views.index, name='index'),
    # path('gestionComptesChefService/', include(router.urls)),
    path('ListDeclaration', ListDeclaration.as_view()),
    # path('DeclarationResponsable', DeclarationResponsable.as_view()),
    path('ListCategory', CategoriesList.as_view()),   
    path('Category/<pk>', CategoryDetailView.as_view()),
    path('Declaration/<pk>', DeclarationDetail.as_view()),
    path('Update_status/<pk>', ToBeApprovedUpdateView.as_view()),
    path('Pending_declarations', ToBeApprovedListView.as_view()),
    path('Rejected_declarations', RejectedListView.as_view()),
    path('Approved_declarations', ApprovedListView.as_view()),
    path('Treated_declarations', TreatedListView.as_view()),
    path('Requested_change_declarations', RequestedChangeListView.as_view()),
    path('drafts', ListDrafts.as_view())



]



