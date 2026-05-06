from django.conf import settings
from django.db import models


class Folder(models.Model):
    INBOX = 'inbox'
    SENT = 'sent'
    TRASH = 'trash'
    ARCHIVE = 'archive'
    SYSTEM_CHOICES = (
        (INBOX, 'Входящие'),
        (SENT, 'Отправленные'),
        (TRASH, 'Корзина'),
        (ARCHIVE, 'Архив'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='folders', verbose_name='Пользователь')
    name = models.CharField(max_length=128, verbose_name='Название')
    system_name = models.CharField(max_length=20, choices=SYSTEM_CHOICES, verbose_name='Системное имя')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        unique_together = ('user', 'system_name')
        verbose_name = 'Папка'
        verbose_name_plural = 'Папки'

    def __str__(self):
        return f'{self.user.username}:{self.name}'
