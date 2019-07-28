# Generated by Django 2.2.3 on 2019-07-24 16:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comments', '0002_comment_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='votes',
            field=models.ManyToManyField(related_query_name='voted_comment', to=settings.AUTH_USER_MODEL),
        ),
    ]