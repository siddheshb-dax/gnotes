from django.contrib.auth import get_user_model
import json
import pytest
from notes.models import Note

@pytest.mark.django_db
def test_note_creation(client):
    user = get_user_model().objects.create_user(
        username="test_user",
        password="Test@123"
    )

    client.force_login(user)

    mutation = """
    mutation CreateNote($title: String!, $content: String!) {
        createNote(title: $title, content: $content) {
            note {
                id
                title
                content
                owner {
                    id
                    username
                }
            }
        }
    }
    """

    TEST_NOTE_TITLE = "This is the title of the note"
    TEST_NOTE_CONTENT = "This is the content of the note."

    variables = {
        "title": TEST_NOTE_TITLE,
        "content": TEST_NOTE_CONTENT
    }

    resp = client.post(
        "/graphql/",
        data = json.dumps({
            "query": mutation,
            "variables": variables,
        }),
        content_type="application/json"
    )

    assert resp.status_code == 200

    payload = resp.json()

    assert "errors" not in payload

    note = payload["data"]["createNote"]["note"]

    assert note["title"] == TEST_NOTE_TITLE
    assert note["content"] == TEST_NOTE_CONTENT
    note_owner = note["owner"]

    assert note_owner["username"] == "test_user"

    assert Note.objects.filter(title=TEST_NOTE_TITLE, content=TEST_NOTE_CONTENT).exists()

