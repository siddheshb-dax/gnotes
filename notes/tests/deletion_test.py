import json
import pytest
from django.contrib.auth import get_user_model

from notes.models import Note

@pytest.mark.django_db
def test_note_delete_mutation(client):
    TEST_NOTE_TITLE = "This is a title of the test note"
    TEST_NOTE_CONTENT = "This is the content of the test note."

    user = get_user_model().objects.create_user(
        username="test",
        password="test"
    )

    note = Note.objects.create(
        title=TEST_NOTE_TITLE,
        content=TEST_NOTE_CONTENT,
        owner=user
    )

    client.force_login(user)

    mutation = """
    mutation DeleteNote($id: ID!) {
        deleteNote(id: $id) {
            success
        }
    }
    """

    variables = {
        "id": str(note.id)
    }

    resp = client.post(
        "/graphql/",
        data = json.dumps({
            "query": mutation,
            "variables": variables,
        }),
        content_type = "application/json"
    )

    assert resp.status_code == 200

    payload = resp.json()
    assert "errors" not in payload

    assert payload["data"]["deleteNote"]["success"] == True

    assert not Note.objects.filter(id=note.id).exists()
