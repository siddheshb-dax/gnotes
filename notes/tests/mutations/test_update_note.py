import json
from django.test import Client
import pytest
from django.contrib.auth import get_user_model

from notes.models import Note

def create_note(t: str, c: str, o):
    created_note = Note.objects.create(
        title=t,
        content=c,
        owner=o
    )

    return created_note

def post(client, query, vars):
    response = client.post(
        "/graphql/",
        data = json.dumps({
            "query": query,
            "variables": vars,
        }),
        content_type="application/json"
    )

    return response


@pytest.mark.django_db
def test_update_note_by_id(client: Client):
    user = get_user_model().objects.create_user(
        username="user", password="pass"
    )

    client.force_login(user)

    _ = create_note("Title 1", "Content 1", user)
    _ = create_note("Title 2", "Content 2", user)
    note_to_update = create_note("Title 4", "Content 4", user)

    mutation = """
    mutation UpdateNoteByID($id: ID!, $t: String, $c: String) {
        updateNote(id: $id, title: $t, content: $c) {
            note {
                id
                title
                content
            }
        }
    }
    """

    note_id = note_to_update.id

    variables = {
        "id": str(note_id),
        "t": "Title 3",
        "c": "Content 3",
    }

    resp = post(client, mutation, variables)

    assert resp.status_code == 200
    payload = resp.json()

    assert "errors" not in payload

    note = payload["data"]["updateNote"]["note"]

    assert note["title"] == "Title 3"
    assert note["content"] == "Content 3"


@pytest.mark.django_db
def test_note_no_change_on_empty_input(client):
    user = get_user_model().objects.create_user(
        username="user", password="pass"
    )
    
    client.force_login(user)
    
    _ = create_note("Title 1", "Content 1", user)
    _ = create_note("Title 2", "Content 2", user)
    note_to_update = create_note("Title 3", "Content 3", user)

    note_id = note_to_update.id

    mutation = """
    mutation UpdateNote($id: ID!, $title: String, $content: String) {
        updateNote(id: $id, title: $title, content: $content) {
            note {
                id
                title
                content
            }
        }
    }
    """

    variables = {
        "id": str(note_id),
        "title": None,
        "content": None,
    }

    resp = post(client, mutation, variables)

    assert resp.status_code == 200
    payload = resp.json()

    assert "errors" not in payload

    note = payload["data"]["updateNote"]["note"]

    assert note["title"] == "Title 3"
    assert note["content"] == "Content 3"


@pytest.mark.django_db
def test_update_only_one_field(client):
    mutation = """
    mutation UpdateNote($id: ID!, $title: String, $content: String) {
        updateNote(id: $id, title: $title, content: $content) {
            note {
                id
                title
                content
            }
        }
    }
    """

    user = get_user_model().objects.create_user(
        username="user", password="pass"
    )
    client.force_login(user)    

    note_1 = create_note("Title 1", "Content", user)
    note_2 = create_note("Title", "Content 2", user)

    variables = {
        "id": str(note_1.id),
        "title": None,
        "content": "Content 1"
    }

    resp = post(client, mutation, variables)

    assert resp.status_code == 200
    assert "errors" not in resp.json()
    assert resp.json()["data"]["updateNote"]["note"]["content"] == "Content 1"

    variables = {
        "id": str(note_2.id),
        "title": "Title 2",
        "content": None
    }

    resp = post(client, mutation, variables) 

    assert resp.status_code == 200
    assert "errors" not in resp.json()
    assert resp.json()["data"]["updateNote"]["note"]["title"] == "Title 2"

