from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('actions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='recipient_deleted',
            field=models.BooleanField(default=False, verbose_name='Удалено получателем'),
        ),
        migrations.AddField(
            model_name='email',
            name='sender_deleted',
            field=models.BooleanField(default=False, verbose_name='Удалено отправителем'),
        ),
    ]
