from .models import Activity

def log(*, user, action, note=None):
    Activity.objects.create(
        user=user,
        action=action,
        note=note,
        note_title=note.title if note else "",
    )
