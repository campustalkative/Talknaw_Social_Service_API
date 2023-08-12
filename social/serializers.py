from rest_framework import serializers
from .models import Post, Comment
from likes.serializers import LikeSerializer


class PostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source = "uid")

    class Meta:
        model = Post
        fields = ["id", "content", "image", "voice_recording", "date_created", "likes" ]

class CreatePostSerializer(serializers.Serializer):
    ...

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ["content","uid", "post_id", "date_created", "likes" ]

class AddCommentSerializer(serializers.Serializer):
    ...


class LikePostSerializer(LikeSerializer):
    post_id = serializers.IntegerField(source="object_id")
    model = Post
    class Meta:
        fields = ['id', 'post_id']


class LikeCommentSerializer (LikeSerializer):
    comment_id = serializers.IntegerField(source="object_id")

    model = Comment
    class Meta:
        fields = ['id', 'comment_id']
