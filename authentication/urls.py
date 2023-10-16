from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import ChangePasswordView, EmailConfirmationView, LoginView, RegisterView, ResendOTPCodeView, ResetPasswordRequestView, ResetPasswordView


router = DefaultRouter()

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('email-confirm/', EmailConfirmationView.as_view(), name='email-confirmation'),
    path('reset-password/request/', ResetPasswordRequestView.as_view(), name='reset-password-request'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('resend-otp-code/', ResendOTPCodeView.as_view(), name='resend-otp-code'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
