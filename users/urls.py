from django.urls import path
from .views import RegisterView, LoginView, UserView,  LogoutView, ChangePasswordView, UpdateProfileView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('change_password', ChangePasswordView.as_view(), name='auth_change_password'),
    path('update_profile', UpdateProfileView.as_view(), name='auth_update_profile'),
]


