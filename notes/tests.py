from django.test import TestCase

# Create your tests here.

import json
import pytest 
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_create_user_mutation_creates_user(client):
    mutation = """
    mutation CreateUser($username: String!, $password: String!) {
        createUser(username: $username, password: $password) {
            user {
                id
                username
            }
        }
    }
    """

    variables = {
        "username": "test_username",
        "password": "Test@123"
    }

    response = client.post(
        "/graphql/",
        data = json.dumps({"query": mutation, "variables": variables}),
        content_type = "application/json"
    )

    assert response.status_code == 200
    payload = response.json()

    assert "errors" not in payload
    user = payload["data"]["createUser"]["user"]

    assert user["username"] == "test_username"
    assert user["id"] is not None

    db_user = get_user_model().objects.get(username="test_username")
    assert db_user.check_password("Test@123")
