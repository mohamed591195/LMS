from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Notify(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    verb         = models.CharField(max_length=50)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id    = models.PositiveIntegerField()
    target       = GenericForeignKey('content_type', 'object_id')
    created_at   = models.DateTimeField(auto_now_add=True)
    read_by      = models.ManyToManyField(User, related_name='read_notifs', related_query_name='notif_readed')
    

    def __str__(self):
        return f'{self.user} {self.verb} {self.target}'

