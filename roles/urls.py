from django.urls import path
from .views import AddRole, UpdateRoleView

urlpatterns = [
    path('add_role', AddRole.as_view()),
    path('edit_role', UpdateRoleView.as_view())
    
]