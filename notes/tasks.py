from celery import shared_task
from .models import Note, Activity
from .services import log

from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def log_activity_task(user_id, action, note_id=None):
    user = User.objects.get(id=user_id)
    note = None

    if note_id:
        note = Note.objects.get(id=note_id) 

    log(
        user=user,
        action=action,
        note=note,
    )
