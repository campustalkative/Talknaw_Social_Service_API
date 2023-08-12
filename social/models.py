from uuid import uuid4

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from hitcount.models import (  #This will add a reverse lookup from HitCount Model
    HitCount,
    HitCountMixin,
)

from likes.models import Like


class Post(models.Model, HitCountMixin):

    uid = models.UUIDField(default=uuid4)

    content = models.TextField()
    image = models.URLField(null=True, blank=True)
    voice_recording = models.URLField(null=True, blank=True)
    user_uid = models.UUIDField() 
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    likes = GenericRelation(Like)

    views = GenericRelation(HitCount, object_id_field="object_pk", related_query_name="views_relation" ) 


    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return self.content[:]
    
    @property
    def clicks(self):
        return self.hit_count.hits


class Comment(models.Model):

    content = models.TextField()
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")

    user_uid = models.UUIDField() 

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    likes = GenericRelation(Like)
