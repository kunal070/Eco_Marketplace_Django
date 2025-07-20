from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.views.generic import CreateView, TemplateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import UserProfile
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import EditProfileForm
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .utils import email_verification_token
import random
from django.core.mail import send_mail
from django.views.generic import FormView
from .forms import PhoneCodeForm
from django.contrib import messages


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('authentication:profile')

    def form_valid(self, form):
        user = form.save()
        profile = UserProfile.objects.create(user=user)
        login(self.request, user)

        # Generate verification token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = email_verification_token.make_token(user)
        domain = get_current_site(self.request).domain
        verification_link = self.request.build_absolute_uri(
            reverse('authentication:verify_email', kwargs={'uidb64': uid, 'token': token})
        )

        # Send verification email
        send_mail(
            subject='Verify your email - Eco-Friendly Marketplace',
            message=f'Hi {user.username},\n\nClick the link below to verify your email:\n{verification_link}',
            from_email='noreply@eco.com',
            recipient_list=[user.email],
            fail_silently=False,
        )

        return redirect('authentication:profile')

class CustomLoginView(LoginView):
    template_name = 'auth/login.html'

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('authentication:login')

class ProfileView(TemplateView):
    template_name = 'auth/profile.html'

class ForgotPasswordView(PasswordResetView):
    template_name = 'auth/forgot_password.html'
    success_url = reverse_lazy('authentication:login')
    email_template_name = 'auth/password_reset_email.html'  # optional

class ResetPasswordView(PasswordResetConfirmView):
    template_name = 'auth/reset_password.html'
    success_url = reverse_lazy('authentication:login')

def verify_email(request, uidb64, token):
    from django.utils.http import urlsafe_base64_decode
    from django.contrib.auth.models import User
    from django.contrib import messages

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user and email_verification_token.check_token(user, token):
        user.userprofile.is_verified = True
        user.userprofile.save()
        messages.success(request, "Your email has been verified!")
    else:
        messages.error(request, "Verification link is invalid or expired.")

    return redirect('authentication:login')

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = EditProfileForm
    template_name = 'auth/edit_profile.html'
    success_url = reverse_lazy('authentication:profile')

    def get_object(self):
        return self.request.user.userprofile

def send_phone_verification_email(request):
    user = request.user
    code = str(random.randint(100000, 999999))
    profile = user.userprofile
    profile.phone_verification_code = code
    profile.is_phone_verified = False
    profile.save()

    send_mail(
        subject="Your Phone Verification Code",
        message=f"Hi {user.username},\n\nYour phone verification code is: {code}",
        from_email="noreply@eco.com",
        recipient_list=[user.email],
        fail_silently=False,
    )

    messages.success(request, "Verification code sent to your email.")
    return redirect('authentication:verify_phone')

class VerifyPhoneView(LoginRequiredMixin, FormView):
    template_name = 'auth/verify_phone.html'
    form_class = PhoneCodeForm
    success_url = reverse_lazy('authentication:profile')

    def form_valid(self, form):
        code = form.cleaned_data['code']
        profile = self.request.user.userprofile

        if profile.phone_verification_code == code:
            profile.is_phone_verified = True
            profile.phone_verification_code = None
            profile.save()
            messages.success(self.request, "Phone number verified!")
        else:
            messages.error(self.request, "Invalid verification code.")

        return super().form_valid(form)