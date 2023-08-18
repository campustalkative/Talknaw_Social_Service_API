from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from likes.views import LikeView
from users.models import Profile
from utils.helpers import custom_cache_decorator

# from .filters import ApartmentFilter
from .models import Comment, Picture, Post, Video
from .pagination import PostPagination
from .serializers import (
    AddCommentSerializer,
    CommentSerializer,
    CreatePostSerializer,
    LikeCommentSerializer,
    LikePostSerializer,
    PostSerializer,
)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    lookup_field = "uid"
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # filterset_class = ApartmentFilter #TODO update this to match this project
    http_method_names = ["get", "post", "patch", "delete"]
    search_fields = ["content"]
    pagination_class = PostPagination
    # ordering_fields = ["category"]

    @action(methods=["GET"], detail=False)
    # @method_decorator(cache_page(timedelta(hours=1).total_seconds()))
    # @method_decorator(vary_on_headers("Authorization",))
    def mine(self, request):
        """
        Returns all the apartments owned by the currently logged in agent

        """
        profile = Profile.objects.get(user_id=request.user_id)

        posts = (
            Post.objects.filter(profile=profile)
            .prefetch_related("pictures", "videos")
            .select_related("profile")
        )

        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return (
            Post.objects.all()
            .select_related("profile")
            .prefetch_related(
                "pictures",
                "videos",
                "comments",
                "profile__watching",
                "profile__watchers",
                "likes",
            )
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreatePostSerializer
        return PostSerializer

    # @method_decorator(custom_cache_decorator)
    def list(self, request: HttpRequest, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request: HttpRequest, *args, **kwargs):
        # Do a hit count

        hit_count = HitCount.objects.get_for_object(self.get_object())

        HitCountMixin.hit_count(request, hit_count)

        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user_id=request.user_id)
        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        images = data.pop("pictures", [])
        videos = data.pop("videos", [])

        new_post = Post.objects.create(**data, profile=profile)

        if images:
            pics = [Picture(image=img, post=new_post) for img in images]

            Picture.objects.bulk_create(pics)

        if videos:
            vids = [Video(clip=clip, post=new_post) for clip in videos]

            Video.objects.bulk_create(vids)

        serializer = PostSerializer(new_post)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LikePostView(LikeView):
    serializer_class = LikePostSerializer

    def post(self, request):
        super().post(request)

        message = "Post liked"
        if self.unlike:
            message = "Post removed like"

        product_instance = Post.objects.get(uid=request.data["post_id"])
        data = PostSerializer(product_instance).data
        return Response(
            {"status": True, "message": message, "result": data},
            status=status.HTTP_200_OK,
        )



class CommentViewSet(ModelViewSet):
    lookup_field = "uid"
    http_method_names = ["get", "post", "patch", "delete"]


    def get_queryset(self):
        post = get_object_or_404(Post, uid=self.kwargs["post_uid"])
        return Comment.objects.filter(post_id=post.id)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCommentSerializer
        return CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = AddCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = get_object_or_404(Profile, user_id=request.user_id)
        content = serializer.validated_data.get("content")
        post_uid = kwargs.get("post_uid")
        post = Post.objects.get(uid=post_uid)

        new_comment = Comment.objects.create(
            content=content, profile=profile, post=post
        )

        serializer = CommentSerializer(new_comment)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeCommentView(LikeView):
    serializer_class = LikeCommentSerializer


    def post(self, request):
        super().post(request)

        message = "Comment liked"
        if self.unlike:
            message = "Comment removed like"

        comment_instance = Comment.objects.get(uid=request.data["comment_id"])
        data = CommentSerializer(comment_instance).data
        return Response(
            {"status": True, "message": message, "result": data},
            status=status.HTTP_200_OK,
        )
