from django.contrib import admin
from .models import Post, Comment, Picture, Video
# Register your models here.


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Picture)
admin.site.register(Video)
