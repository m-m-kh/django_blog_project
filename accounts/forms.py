from django.contrib.auth.forms import UserCreationForm, UserChangeForm, BaseUserCreationForm

from accounts.models import CustomUser
from django import forms
from django.utils.translation import gettext as _

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = "__all__"

