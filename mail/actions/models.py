from django.conf import settings
from django.db import models

from folders.models import Folder


class Email(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_emails")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_emails")
    subject = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sender_folder = models.ForeignKey(Folder, on_delete=models.PROTECT, related_name="outbox_emails")
    recipient_folder = models.ForeignKey(Folder, on_delete=models.PROTECT, related_name="inbox_emails")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} ({self.sender_id}->{self.recipient_id})"
