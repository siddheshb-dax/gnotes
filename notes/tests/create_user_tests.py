from django.test import TestCase

# Create your tests here.

import json
import pytest 
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_create_user_mutation_creates_user(client):

    # Define the mutation for creating a user
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

    # Define the values to pass 
    variables = {
        "username": "test_username",
        "password": "Test@123"
    }

    # Send the request passing the values and get the resposnse
    response = client.post(
        "/graphql/",
        data = json.dumps({"query": mutation, "variables": variables}),
        content_type = "application/json"
    )

    # Assert successful request
    assert response.status_code == 200

    # Extract the payload from the response 
    payload = response.json()

    # Assert no errors in the response
    assert "errors" not in payload

    # Fetch the user object from the executed mutation
    user = payload["data"]["createUser"]["user"]

    # Assert correct username
    assert user["username"] == "test_username"

    # assert that the ID of the created user is not none
    assert user["id"] is not None

    # Fetch the user from the Test DB
    db_user = get_user_model().objects.get(username="test_username")

    '''
        check_password fetches the same salt and hashing algorithm
        and matches the hashed password for the user
    '''
    assert db_user.check_password("Test@123")

@pytest.mark.django_db
def test_create_user_without_password_fails(client):
    mutation = """
    mutation CreateUserWithoutPassword($username: String!, $pw: String!) {
        createUser(username: $username, password: $pw) {
            user {
                username
            }
        }
    }
    """

    variables = {
        "username": "test_username"
        # pw missing
    }

    response = client.post(
        "/graphql/",
        data = json.dumps({
            "query": mutation,
            "variables": variables
        }),
        content_type = "application/json"
    )

    # changed from 200 as graphene resolves the request strictly based on internal
    # schema, we expect a 400 error code here. 
    assert response.status_code == 400 

    payload = response.json()

    assert "errors" in payload

    assert not get_user_model().objects.filter(username="test_username").exists()

