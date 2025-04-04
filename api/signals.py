from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Image

@receiver(post_save, sender=Image)
def notify_admin_on_new_upload(sender, instance, created, **kwargs):
    if created:
        subject = "📢 New Image Uploaded!"
        message = f"A new image has been uploaded in Container: {instance.container.container_number}.\n\nImage Path: {instance.image.url}"
        
        # Replace this with your admin email
        admin_email = "admin@example.com"

        send_mail(
            subject,
            message,
            "noreply@digiconapp.com",
            [admin_email],
            fail_silently=False,
        )
