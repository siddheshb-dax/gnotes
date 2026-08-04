import json 
import pytest
from django.contrib.auth import get_user_model
from notes.models import Note

def create_note(t: str, c: str, o):
    Note.objects.create(
        title=t,
        content=c,
        owner=o
    )

def post(client, query, vars):
    resp = client.post(
        "/graphql",
        data = json.dumps({
            "query": query,
            "variables": vars
        }),
        content_type="application/json"
    )

    return resp

@pytest.mark.django_db
def test_filter_single(client):
    user = get_user_model().objects.create_user(
        username="user",
        password="pass"
    )

    client.force_login(user)

    create_note(
        t="Title",
        c="Content",
        o=user
    )

    create_note(
        t="Gibberish",
        c="Gibberish",
        o=user
    )

    create_note(
        t="Hello World",
        c="hello!",
        o=user
    )

    query = """
    query FetchNotesWithFilters($t: String, $c: String) {
        notes (title: $t, content: $c) {
            id
            title
            content
        }
    }
    """

    v1 = {
        "t": "Title"
    }

    v2 = {}

    resp = post(client, query, v1)
    assert resp.status_code == 200
    payload = resp.json()
    assert "errors" not in payload
    note_v1 = payload["data"]["notes"]
    assert len(note_v1) == 1    

    resp = post(client, query, v2)
    assert resp.status_code == 200
    payload = resp.json()
    assert "errors" not in payload
    note_v2 = payload["data"]["notes"]
    assert len(note_v2) == 3
