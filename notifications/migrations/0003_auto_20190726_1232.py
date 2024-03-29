# Generated by Django 2.2.3 on 2019-07-26 12:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0002_notify_read'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notify',
            name='read',
        ),
        migrations.AddField(
            model_name='notify',
            name='read_by',
            field=models.ManyToManyField(related_name='read_notifs', related_query_name='notif_readed', to=settings.AUTH_USER_MODEL),
        ),
    ]
