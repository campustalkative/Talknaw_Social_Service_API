from django.http.request import HttpRequest
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from likes.views import LikeView
from utils.helpers import custom_cache_decorator

from .filters import ApartmentFilter
from .models import Comment, Post
from .serializers import (
    AddCommentSerializer,
    CommentSerializer,
    LikeCommentSerializer,
    LikePostSerializer,
    PostSerializer,
)


class PostView(ModelViewSet):

    queryset = Post.objects.all()
    lookup_field = 'uid'
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ApartmentFilter #TODO update this to match this project
    http_method_names = ["get", "post", "put", "delete"]
    search_fields = ["address", "price", "category", "title"]
    ordering_fields = ["category"]

    def get_serializer_class(self):
        return 
    
    @method_decorator(custom_cache_decorator)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request: HttpRequest, *args, **kwargs):

        # Do a hit count

        hit_count = HitCount.objects.get_for_object(self.get_object())

        HitCountMixin.hit_count(request, hit_count)

        return super().retrieve(request, *args, **kwargs)
    

class LikePostView (LikeView):
    serializer_class = LikePostSerializer

    def post(self, request):
        super().post(request)

        message = "Post liked"
        if self.unlike:
            message = "Post removed like"

        product_instance = Post.objects.get(id=request.data["post_id"])
        data = PostSerializer(product_instance).data
        return Response(
            {"status": True, "message": message, "results": data},
            status=status.HTTP_200_OK,
        )


class CommentViewSet(ModelViewSet):

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk'])

    def get_serializer_context(self):
        return {'user': self.request.user, 'post_id': self.kwargs['post_pk']}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCommentSerializer
        return CommentSerializer

class LikeCommentView(LikeView):
    serializer_class = LikeCommentSerializer