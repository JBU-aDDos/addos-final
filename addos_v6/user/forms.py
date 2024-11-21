from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    nickname = forms.CharField(max_length=30, required=True, label='Nickname')
    ip_address = forms.GenericIPAddressField(protocol='both', unpack_ipv4=False, required=True, label='IP Address')

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'nickname', 'ip_address')

class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')