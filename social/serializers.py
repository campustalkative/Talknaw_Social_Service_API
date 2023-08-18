from rest_framework import serializers

from likes.serializers import LikeSerializer
from likes.models import Like
from users.views import ProfileSerializer

from .models import Comment, Picture, Post, Video


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ["image"]


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ["clip"]


class PostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="uid")
    pictures = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    profile = ProfileSerializer()

    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "voice_recording",
            "date_created",
            "comment_count",
            "like_count",
            "pictures",
            "videos",
            "profile",
        ]

    def get_pictures(self, obj):
        return [picture.image for picture in obj.pictures.all()]

    def get_videos(self, obj):
        return [video.clip for video in obj.videos.all()]


class CreatePostSerializer(serializers.Serializer):
    content = serializers.CharField()
    pictures = serializers.ListField(child=serializers.CharField())
    videos = serializers.ListField(child=serializers.CharField())
    voice_recording = serializers.CharField()




class CommentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="uid")
    profile = ProfileSerializer()

    class Meta:
        model = Comment
        fields = ["id", "content", "date_created", "like_count", "profile"]


class AddCommentSerializer(serializers.Serializer):
    content = serializers.CharField()


class LikePostSerializer(LikeSerializer):
    post_id = serializers.UUIDField(source="object_id")
    model = Post

    class Meta:
        model = Like
        fields = ["id", "post_id"]


class LikeCommentSerializer(LikeSerializer):
    comment_id = serializers.UUIDField(source="object_id")
    model = Comment

    class Meta:
        model = Like
        fields = ["id", "comment_id"]
