from django.urls import path
from .views import AddRole

urlpatterns = [
    path('add_role', AddRole.as_view())
]