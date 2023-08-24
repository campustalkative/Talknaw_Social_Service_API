from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from . import views

router  =  DefaultRouter(trailing_slash=False)

router.register("posts", views.PostViewSet, basename="posts")

nested_router = NestedDefaultRouter(router, "posts", lookup="post")

nested_router.register("comments", views.CommentViewSet, basename="posts-comments")

urlpatterns = [
    path("like/post", views.LikePostView.as_view()),
    path("like/comment", views.LikeCommentView.as_view()),
    path("bookmark", views.BookmarkView.as_view())

 

] + router.urls + nested_router.urls
