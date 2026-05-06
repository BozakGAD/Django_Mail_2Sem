from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [('folders', '0001_initial'), ('users', '0001_initial')]
    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_emails', to='users.user')),
                ('recipient_folder', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inbox_emails', to='folders.folder')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_emails', to='users.user')),
                ('sender_folder', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='outbox_emails', to='folders.folder')),
            ],
            options={'ordering': ['-created_at']},
        )
    ]
