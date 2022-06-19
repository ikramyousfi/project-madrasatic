from django.urls import path
from .views import *
from rest_framework import routers
from django.urls import include

from .views import RegisterView, LoginView, UserView,  LogoutView, VerifyEmail,Deactivate_account, ChangePasswordView, UpdateProfileView,RequestPasswordResetEmailView,SetNewPasswordAPIView,PasswordTokenCheckAPI,RoleView

urlpatterns = [
<<<<<<< HEAD
    path('gestionComptes/', include(router.urls)),
   
=======
>>>>>>> 5e0ce5c03ecea39e5e56b12921703152fb47de69
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('emailverify', VerifyEmail.as_view(), name='emailverify'),

    path('change_password', ChangePasswordView.as_view(), name='auth_change_password'),
    path('update_profile', UpdateProfileView.as_view(), name='auth_update_profile'),
    
    path('deactivate_profile', Deactivate_account.as_view(), name='auth_deactivate_profile'),
    path('request_reset_email/', RequestPasswordResetEmailView.as_view(),
         name="request-reset-email"),
    path('password_reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password_reset_complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
     path('roles', RoleView.as_view()),
     path('delete_role/<pk>', DeleteRoleView.as_view()),

     path('roles_assignment', RoleAssignmentView.as_view()),
     path('unassign_role/<pk>', UnassignRoleView.as_view()),


]

