from django.urls import path
from .views import ListDeaclaration , CategoriesList, CategoryDetailView


urlpatterns = [
    path('create_declaration', ListDeaclaration.as_view()),
    path('ListCategory', CategoriesList.as_view()),   
    path('Category/<pk>', CategoryDetailView.as_view())
 
]



