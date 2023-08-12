import os

import dj_database_url

from .settings import *

SECRET_KEY = os.environ.get("SECRET_KEY", config("SECRET_KEY", SECRET_KEY))

DEBUG = config("DEBUG", False, cast = bool)

ALLOWED_HOSTS = []

CSRF_TRUSTED_ORIGINS = ["https://" + host for host in ALLOWED_HOSTS]

# DATABASES = {"default": dj_database_url.config()}
DATABASES = {
    "default": dj_database_url.parse(
        config("DATABASE_URL", ""),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

INSTALLED_APPS.remove("debug_toolbar")
MIDDLEWARE.remove("debug_toolbar.middleware.DebugToolbarMiddleware")


STORAGES = {
    "default":{
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles":{
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"
    }
}

REDIS_URL = ""

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
    }
}
