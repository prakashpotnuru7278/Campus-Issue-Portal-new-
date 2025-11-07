from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Issue, Notification

@receiver(pre_save, sender=Issue)
def send_status_update_notification(sender, instance, **kwargs):
    """
    Sends a notification to the student ONLY if the status changes.
    """
    if not instance.pk:
        # New issue being created, don't notify
        return

    try:
        previous = Issue.objects.get(pk=instance.pk)
    except Issue.DoesNotExist:
        return

    if previous.status != instance.status and instance.student:
        Notification.objects.create(
            user=instance.student,  # This must match your Notification model field
            message=f"Your issue '{instance.title}' status changed from {previous.status} to {instance.status}."
        )
