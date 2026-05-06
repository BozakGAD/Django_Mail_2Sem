from django.conf import settings
from django.db import models

from folders.models import Folder


class Email(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_emails', verbose_name='Отправитель')

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_emails', verbose_name='Получатель')

    subject = models.CharField(max_length=255, verbose_name='Тема')
    body = models.TextField(verbose_name='Текст')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    sender_folder = models.ForeignKey(Folder, on_delete=models.PROTECT, related_name='outbox_emails', verbose_name='Папка отправителя')

    recipient_folder = models.ForeignKey(Folder, on_delete=models.PROTECT, related_name='inbox_emails', verbose_name='Папка получателя')
    
    sender_deleted = models.BooleanField(default=False, verbose_name='Удалено отправителем')
    recipient_deleted = models.BooleanField(default=False, verbose_name='Удалено получателем')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'

    def __str__(self):
        return f'{self.subject} ({self.sender_id}->{self.recipient_id})'
