from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=550, unique=True)


class Profile(models.Model):
    user_id = models.UUIDField()
    name = models.CharField(max_length=550)
    username = models.CharField(max_length=550)
    picture = models.CharField(max_length=550, null=True, blank=True)
    bio = models.CharField(max_length=1000, null=True, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)

    class Meta:
        indexes = [models.Index(fields=["username"]), models.Index(fields=["user_id"])]

    @property
    def watchers_count(self):
        return self.watchers.count()

    @property
    def watching_count(self):
        return self.watching.count()


class UserWatching(models.Model):
    user_id = models.ForeignKey(
        Profile, related_name="watching", on_delete=models.CASCADE
    )
    watching_user_id = models.ForeignKey(
        Profile, related_name="watchers", on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "watching_user_id"], name="unique_watchers"
            )
        ]
        indexes = [
            models.Index(fields=["user_id"]),
            models.Index(fields=["watching_user_id"]),
        ]
        ordering = ["-date_created"]

    def __str__(self):
        f"{self.user_id} follows {self.watching_user_id}"
