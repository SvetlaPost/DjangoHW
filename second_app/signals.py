from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Task

@receiver(pre_save, sender=Task)
def notify_user_on_status_change(sender, instance, **kwargs):
    if not instance.pk:

        return

    try:
        old_task = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        return

    if old_task.status != instance.status:
        subject = f"The current status of your task '{instance.title}' updated"
        message = f"The new one is: {instance.get_status_display()}"
        recipient = instance.owner.email

        if recipient:
            send_mail(subject, message, None, [recipient])
