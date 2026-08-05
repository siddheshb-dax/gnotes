from django.db import models

# Create your models here.

from django.conf import settings

class Note(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notes'
    )

    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or 'Untitled Note'

class Activity(models.Model):
    class Action(models.TextChoices):
        CREATE = "CREATE", "Create"
        UDPATE = "UPDATE", "Update"
        DELETE = "DELETE", "Delete"
        LOGIN = "LOGIN", "Login"
        IMPORT = "IMPORT", "Import"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activities"
    )

    action = models.CharField(
        max_length=20,
        choices=Action.choices
    )

    note = models.ForeignKey(
        Note,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activities"
    )

    note_title = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        if self.note:
            return f"{self.user.username} {self.action} note #{self.note.id}"

        return f"{self.user.username} {self.action}"
