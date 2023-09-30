from rest_framework import serializers


class ProfileSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    name = serializers.CharField()
    username = serializers.CharField()
    picture = serializers.CharField(allow_blank=True)
    bio = serializers.CharField(allow_blank=True)
    watchers_count = serializers.IntegerField()
    watching_count = serializers.IntegerField()
    user_skills = serializers.JSONField()
    date_created = serializers.DateTimeField()
    is_verified = serializers.BooleanField()


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


class SkillSerializer(serializers.Serializer):
    names = serializers.ListField(child=serializers.CharField())
