from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile, UserWatching


class ProfileSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    name = serializers.CharField()
    username = serializers.CharField()
    picture = serializers.CharField(allow_blank=True)
    bio = serializers.CharField(allow_blank=True)
    watchers_count = serializers.IntegerField()
    watching_count = serializers.IntegerField()


class ProfileUpdateSerializer(serializers.Serializer):
    picture = serializers.CharField(allow_blank=True)
    bio = serializers.CharField(allow_blank=True)

    def save(self, **kwargs):
        data = {k: v for k, v in self.validated_data.items() if v}

        if data:
            for k, v in data.items():
                setattr(self.instance, k, v)

        return self.instance.save()


class UserWatchSerializer(serializers.Serializer):
    watching_user_id = serializers.UUIDField()


class ProfileView(GenericAPIView):
    def get(self, request):
        profile = Profile.objects.get(user_id=request.user_id)

        serializer = ProfileSerializer(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        profile = Profile.objects.get(user_id=request.user_id)
        serializer = ProfileUpdateSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return ProfileUpdateSerializer
        return ProfileSerializer


class GetWatchers(APIView):
    """
    Get list of user's Following you.
    """

    def get(self, request):
        user_profile = get_object_or_404(Profile, user_id=request.user_id)

        results = UserWatching.objects.filter(user_id=user_profile)

        ids = [profile.watching_user_id.user_id for profile in results]

        profiles = Profile.objects.filter(user_id__in=ids)

        serializer = ProfileSerializer(profiles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetWatching(APIView):
    """
    Get the list of profile you are following
    """

    def get(self, request):
        user_profile = get_object_or_404(Profile, user_id=request.user_id)

        results = UserWatching.objects.filter(user_id=user_profile)

        # TODO change the name of the field on the Userwatching model, it is confusing
        ids = [profile.user_id.user_id for profile in results]

        profiles = Profile.objects.filter(user_id__in=ids)

        serializer = ProfileSerializer(profiles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class StartWatching(APIView):
    """
    Start Following a user by passing the profile's user_id
    """

    serializer_class = UserWatchSerializer

    def post(self, request):
        serializer = UserWatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_profile = get_object_or_404(Profile, user_id=request.user_id)
        other_user_profile = get_object_or_404(
            Profile, user_id=serializer.validated_data["watching_user_id"]
        )
        UserWatching.objects.create(
            user_id=user_profile,
            watching_user_id=other_user_profile,
        )

        serializer = ProfileSerializer(other_user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StopWatching(APIView):
    """
    Unfollow a particular user by passing the user_id
    """

    def delete(self, request, user_id):
        user_profile = get_object_or_404(Profile, user_id=request.user_id)
        other_user_profile = get_object_or_404(Profile, user_id=user_id)

        watch_obj = get_object_or_404(
            UserWatching, user_id=user_profile, watching_user_id=other_user_profile
        )

        watch_obj.delete()

        serializer = ProfileSerializer(other_user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
