from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from notifications.models import Notify

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'object_id')
    replies = GenericRelation('self', content_type_field='content_type', object_id_field='object_id', related_query_name='on_comment')
    created_at = models.DateTimeField(auto_now_add=True)
    votes = models.ManyToManyField(User, related_query_name='voted_comment')
    notifications = GenericRelation(Notify, content_type_field='content_type', object_id_field='object_id', related_query_name='on_comment')
  
  
    def __str__(self):
        return self.comment[:20]

