from django.contrib import admin
from .models import Profile,Otp

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (['id', 'email', 'is_superuser'])


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ['otp_data', 'user']