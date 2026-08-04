import json
import pytest

from django.contrib.auth import get_user_model

from notes.models import Note

def helper_create_note(title: str, content: str, owner):
    Note.objects.create(
        title=title,
        content=content,
        owner=owner
    )

def helper_create_user(username: str, password: str):
    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )

    return user

@pytest.mark.django_db
def test_list_all_notes(client):
    query = """
    query {
        notes {
            id
            title
            content
        }
    }
    """

    USER_1_IT = 4
    USER_2_IT = 5

    user1 = helper_create_user("user1", "pass")
    user2 = helper_create_user("user2", "pass")

    for i in range(USER_1_IT):
        helper_create_note(
            title=f"Title {i + 1} for user1",
            content=f"Content {i + 1} for user1",
            owner=user1
        )

    client.force_login(user=user1)

    user1_resp = client.post(
        "/graphql/",
        data = json.dumps({
            "query": query,
        }),
        content_type="application/json"
    )

    assert user1_resp.status_code == 200

    payload_user1 = user1_resp.json()

    notes_for_user1 = payload_user1["data"]["notes"]
    assert len(notes_for_user1) == USER_1_IT

    for i in range(USER_1_IT):
        assert notes_for_user1[i]["title"] == f"Title {i + 1} for user1"
        assert notes_for_user1[i]["content"] == f"Content {i + 1} for user1"

    for i in range(USER_2_IT):
        helper_create_note(
            title=f"Title {i + 1} for user2",
            content=f"Content {i + 1} for user2",
            owner=user2
        )

    client.force_login(user=user2)

    user2_resp = client.post(
        "/graphql/",
        data = json.dumps({
            "query": query
        }),
        content_type = "application/json"
    )

    assert user2_resp.status_code == 200
    payload_user2 = user2_resp.json()

    notes_for_user2 = payload_user2["data"]["notes"]
    assert len(notes_for_user2) == USER_2_IT

    for i in range(USER_1_IT):
        assert notes_for_user2[i]["title"] == f"Title {i + 1} for user2"
        assert notes_for_user2[i]["content"] == f"Content {i + 1} for user2"

