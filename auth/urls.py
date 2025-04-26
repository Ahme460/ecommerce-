from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path("refresh/", TokenRefreshView.as_view(), name="TokenRefreshView"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('send-reset-code/', SendResetCodeView.as_view(), name='send_reset_code'),
    path('check-reset-code/', CheckResetCodeView.as_view(), name='check_reset_code'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]
##