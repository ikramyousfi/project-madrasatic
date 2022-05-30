from django.urls import path
from .views import *
from rest_framework import routers
from django.urls import include

router = routers.DefaultRouter()
router.register(r'roles', roleView, basename='roles')


urlpatterns = [
    path('gestionComptes/', include(router.urls)),
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('emailverify', VerifyEmail.as_view(), name='emailverify'),

    path('change_password', ChangePasswordView.as_view(), name='auth_change_password'),
    path('update_profile', UpdateProfileView.as_view(), name='auth_update_profile'),
    
    path('request_reset_email/', RequestPasswordResetEmailView.as_view(),
         name="request-reset-email"),
    path('password_reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password_reset_complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete')
]

