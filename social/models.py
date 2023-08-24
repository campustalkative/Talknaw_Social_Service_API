from uuid import uuid4

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from hitcount.models import (  # This will add a reverse lookup from HitCount Model
    HitCount,
    HitCountMixin,
)

from likes.models import Like
from users.models import Profile


class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(BaseModel, HitCountMixin):
    uid = models.UUIDField(default=uuid4, editable=False)

    content = models.TextField()
    voice_recording = models.CharField(max_length=500, null=True, blank=True)
    # user_id = models.UUIDField()
    expiry = models.DateTimeField(null=True)
    likes = GenericRelation(Like)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")

    views = GenericRelation(
        HitCount, object_id_field="object_pk", related_query_name="views_relation"
    )

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return self.content[:]

    # @property
    # def views(self):
    #     return self.hit_count.hits

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        if self.comments:
            return self.comments.count()
        return None


class Picture(BaseModel):
    image = models.CharField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="pictures")


class Video(BaseModel):
    clip = models.CharField(max_length=500, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="videos")


class Comment(BaseModel):
    uid = models.UUIDField(default=uuid4, editable=False)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="comments"
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    likes = GenericRelation(Like)

    @property
    def like_count(self):
        return self.likes.count()


class Bookmark(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id  = models.UUIDField()
