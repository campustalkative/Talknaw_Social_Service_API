from uuid import UUID

from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend
from django.shortcuts import redirect
from ninja import NinjaAPI, Schema

from users.models import Profile

api = NinjaAPI(csrf=False)


class ChangeUsername(Schema):
    username: str
    user_id: UUID


class ProfileSchema(ChangeUsername):
    user_id: UUID
    name: str
    username: str
    picture: str = None


@api.post("create/profile")
def create_profile(request, profile_data: ProfileSchema):
    Profile.objects.create(**profile_data.dict())
    return {"status": "New profile created"}


@api.post("update/username")
def update_username(request, username_data: ChangeUsername):
    profile = Profile.objects.get(user_id=username_data.user_id)
    profile.username = username_data.username
    profile.save()
    return {"status": "Username updated successfully"}


def return_home_to_docs(request):
    return redirect("swagger-schema")
