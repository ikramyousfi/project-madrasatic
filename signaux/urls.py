from django.urls import path
from .views import addSignal


urlpatterns = [
    path('signal', addSignal.as_view()),
    #path('categorie', displayCategorie.as_view())
    
]
