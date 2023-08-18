from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from ninja import Router

from .models import Like
from .schema import LikeSchema

router = Router()
User = get_user_model()


@router.post("/like")
def like_view(request, payload: LikeSchema, user: User = None):
    try:
        obj = get_object_or_404(Like.content_type.model_class(), id=payload.object_id)
    except Like.content_type.model_class().DoesNotExist:
        return {"error": f"{Like.content_type.model_class().__name__} does not exist"}

    content_type = ContentType.objects.get_for_model(Like.content_type.model_class())

    if like := Like.objects.filter(
        user_id=user.id, object_id=payload.object_id, content_type=content_type
    ):
        like.delete()
        return {"message": "Unlike successful"}

    Like.objects.create(
        user_id=user.id,
        content_type=content_type,
        object_id=payload.object_id,
        content_object=obj,
    )
    return {"message": "Like successful"}
