"""
URL configuration for Talknaw project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.conf import settings
from django.conf.urls.static import static
from core.views import api, return_home_to_docs

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", return_home_to_docs),
    path("", include("social.urls")),
    path("", include("users.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api/", api.urls),
]

# # Documentation paths

urlpatterns += [
    # YOUR PATTERNS 
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/docs/spec",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-schema",
    ),
    path(
        "api/redocs/spec",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc-schema",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
