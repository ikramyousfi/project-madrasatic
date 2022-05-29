from django.urls import path
from .views import addSignal , CategoriesList, CategoryDetailView


urlpatterns = [
    path('add_signal', addSignal.as_view()),
    path('ListCategory', CategoriesList.as_view()),   
    path('Category/<pk>', CategoryDetailView.as_view())
 
]



