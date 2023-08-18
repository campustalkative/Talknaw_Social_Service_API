from django.urls import path

from . import views

urlpatterns = [
    path("profile", views.ProfileView.as_view()),
    path("watchers", views.GetWatchers.as_view()),
    path("watching", views.GetWatching.as_view()),
    path("watch", views.StartWatching.as_view()),
    path("unwatch/<uuid:user_id>", views.StopWatching.as_view()),
]
