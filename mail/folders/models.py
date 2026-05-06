from django.conf import settings
from django.db import models


class Folder(models.Model):
    INBOX = "inbox"
    SENT = "sent"
    TRASH = "trash"
    ARCHIVE = "archive"
    SYSTEM_CHOICES = (
        (INBOX, "Inbox"),
        (SENT, "Sent"),
        (TRASH, "Trash"),
        (ARCHIVE, "Archive"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="folders")
    name = models.CharField(max_length=128)
    system_name = models.CharField(max_length=20, choices=SYSTEM_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "system_name")

    def __str__(self):
        return f"{self.user.username}:{self.name}"
