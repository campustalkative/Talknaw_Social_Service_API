from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey



class LikesManager(models.Manager):
    def get_likes_for(self, content_object, object_id):
        query = ContentType.objects.get_for_model(content_object, object_id)
        return query
    
    def objects_liked_by_user(self, user, content_object):
        content_type = ContentType.objects.get_for_model(content_object)
        likes = self.filter(
            content_type = content_type, 
            user = user
        )

        _ids = [item.object_id for item in likes]
        
        return content_object.objects.filter(pk__in = _ids)


class Like(models.Model):
    objects = LikesManager
    user_uid = models.UUIDField() 
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

