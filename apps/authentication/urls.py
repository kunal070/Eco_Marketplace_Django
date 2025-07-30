from django.urls import path
from .views import (
    ResetPasswordView,
    verify_email,
    EditProfileView,
    send_phone_verification_email,
    VerifyPhoneView,
    ForgotPasswordPhoneView,
    VerifyOtpAndResetPasswordView,
)
from . import views

app_name = 'authentication'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),

    # Phone-based password reset
    path('forgot-password-phone/', ForgotPasswordPhoneView.as_view(), name='forgot_password_phone'),
    path('verify-otp-reset/', VerifyOtpAndResetPasswordView.as_view(), name='verify_otp_reset'),

    # Email verification
    path('verify/<uidb64>/<token>/', verify_email, name='verify_email'),

    # Profile management
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    path('send-phone-code/', send_phone_verification_email, name='send_phone_code'),
    path('verify-phone/', VerifyPhoneView.as_view(), name='verify_phone'),
]
