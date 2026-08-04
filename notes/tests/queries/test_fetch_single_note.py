import json
import pytest

from django.contrib.auth import get_user_model
from notes.models import Note

def helper_create_note(t: str, c: str, o):
    Note.objects.create(
        title=t,
        content=c,
        owner=o
    )

def create_user(id: str, pw: str):
    user = get_user_model().objects.create_user(
        username=id,
        password=pw
    )

    return user

@pytest.mark.django_db
def test_fetch_single_note_with_id(client):
    user = create_user(id="user", pw="pass")

    query = """
    query GetSingleNote($id: ID!) {
        note (id: $id) {
            id
            title
            content
        }
    }
    """

    USER_IT = 5
    ID_TO_FETCH = 3

    for i in range(USER_IT):
        if i == ID_TO_FETCH:
            n = Note.objects.create(
                title=f"Title {i + 1}",
                content=f"Content {i + 1}",
                owner=user
            )

            note_id = n.id
            note_title = n.title
            note_content = n.content

        helper_create_note(
            t=f"Title {i + 1}",
            c=f"Content {i + 1}",
            o=user
        )

    client.force_login(user=user)

    resp = client.post(
        "/graphql/",
        data = json.dumps({
            "query": query,
            "variables": {
                "id": note_id
            }
        }),
        content_type="application/json",
    )

    assert resp.status_code == 200

    payload = resp.json()

    assert "errors" not in payload

    note = payload["data"]["note"]

    assert note["id"] == str(note_id)
    assert note["title"] == note_title
    assert note["content"] == note_content


@pytest.mark.django_db
def test_fetch_single_note_id_dne(client):
    user = create_user(id="user", pw="pass")

    query = """
    query {
        note (id: 9999) {
            id
            title
            content
        }
    }
    """

    helper_create_note(
        t="Title 1",
        c="Content 1",
        o=user
    )

    client.force_login(user=user)

    resp = client.post(
        "/graphql/",
        data=json.dumps({
            "query": query
        }),
        content_type="application/json",
    )

    assert resp.status_code == 200

    payload = resp.json()

    assert "errors" not in payload

    assert payload["data"]["note"] is None
