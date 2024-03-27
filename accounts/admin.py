from django.contrib import admin


from accounts.models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import AbstractUser, User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_id','email_confirmed')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name', 'profile_id','email_confirmed')}),
    )