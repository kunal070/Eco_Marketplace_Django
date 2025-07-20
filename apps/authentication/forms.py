from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'bio', 'location', 'phone_number')

class PasswordResetForm(DjangoPasswordResetForm):
    email = forms.EmailField(label="Enter your email", max_length=254)

class EmailVerificationForm(forms.Form):
    code = forms.CharField(max_length=6, label="Enter verification code")


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio', 'location', 'phone_number', 'preferences']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

class PhoneCodeForm(forms.Form):
    code = forms.CharField(max_length=6, label="Enter the 6-digit code")