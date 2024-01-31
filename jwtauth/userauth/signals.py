from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Otp


@receiver(post_save, sender=Otp)
def otp_generated(sender, instance, created, **kwargs, ):

    if created:
        print("OTP generated")
        send_mail(
            "OTP For Forget Pasword",
            f"Your OPT:-   {instance.otp_data}",
            settings.EMAIL_HOST_USER,
            [instance.user],
            fail_silently=False
        )