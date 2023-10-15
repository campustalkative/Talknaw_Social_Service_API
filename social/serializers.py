from rest_framework import serializers

from likes.models import Like
from likes.serializers import LikeSerializer
from users.views import ProfileSerializer

from .models import Bookmark, Comment, Picture, Post, Video


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
        return [picture.image.url for picture in obj.pictures.all()]

    def get_videos(self, obj):
        return [video.clip.url for video in obj.videos.all()]


class CreatePostSerializer(serializers.Serializer):
    content = serializers.CharField()
    pictures = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=True, required=False),
        allow_empty=True,
        required=False,
    )
    videos = serializers.ListField(
        child=serializers.FileField(allow_empty_file=True, required=False),
        allow_empty=True,
        required=False,
    )
    voice_recording = serializers.FileField(allow_empty_file=True, required=False)


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


class CreateBookmarkSerializer(serializers.Serializer):
    post_id = serializers.UUIDField()
