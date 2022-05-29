from django.urls import path
from .views import ListDeaclaration , CategoriesList, CategoryDetailView, DeclarationDetail


urlpatterns = [
    path('ListDeclaration', ListDeaclaration.as_view()),
    path('ListCategory', CategoriesList.as_view()),   
    path('Category/<pk>', CategoryDetailView.as_view()),
    path('Declaration/<pk>', DeclarationDetail.as_view())

 
]



