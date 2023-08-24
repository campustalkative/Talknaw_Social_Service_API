from ninja import NinjaAPI
from users.models import Profile
from ninja import Schema
from uuid import UUID
from django.shortcuts import redirect

api = NinjaAPI(csrf=False)

class ProfileSchema(Schema):
    user_id: UUID
    name:str
    username: str
    picture: str = None


@api.post("create/profile")
def create_profile(request, profile_data: ProfileSchema):

    Profile.objects.create(**profile_data.dict())
    return{"status": "New profile created"}



def return_home_to_docs(request):
    return redirect("swagger-schema")
 