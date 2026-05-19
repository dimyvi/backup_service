from django.db import models
from django.contrib.auth.models import User

class Backup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='backups/')
    size = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class ActivityLog(models.Model):

    ACTIONS = (
        ("uploaded", "Uploaded"),
        ("deleted", "Deleted"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    action = models.CharField(
        max_length=20,
        choices=ACTIONS
    )

    filename = models.CharField(max_length=255)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]