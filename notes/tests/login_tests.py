import json
import pytest
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_login_mutation(client):

    # Create a user with the ORM
    user = get_user_model().objects.create_user(
        username = "test_user",
        password = "Test@123"
    )

    # Define a successful login mutation 
    mutation = """
    mutation Login($name: String!, $pw: String!) {
        login(username: $name, password: $pw) {
            success
            user {
                username
            }
        }
    }
    """

    # Define the user credentials
    variables = {
        "name": "test_user",
        "pw": "Test@123"
    }

    # Send the request to log a user in
    response = client.post(
        "/graphql/",
        data = json.dumps({
            "query": mutation,
            "variables": variables
        }),
        content_type="application/json"
    )

    # Assertions
    assert response.status_code == 200
    payload = response.json()

    assert "errors" not in payload

    assert payload["data"]["login"]["success"] == True
    assert payload["data"]["login"]["user"]["username"] == "test_user"


@pytest.mark.django_db
def test_login_with_incorrect_creds(client):
    # Create a test user
    user = get_user_model().objects.create_user(
        username="test",
        password="test"
    )

    # Create the login mutation
    mutation = """
    mutation LoginWithWrongCreds($name: String!, $pw: String!) {
        login(username: $name, password: $pw) {
            success
            user {
                username
            }
        }
    }
    """

    variables = {
        "name": "test",
        "pw": "wrong_password"
    }

    resp = client.post(
        "/graphql/",
        data = json.dumps({
            "query": mutation,
            "variables": variables,
        }),
        content_type="application/json"
    )

    payload = resp.json()

    '''
        It is expected that the response code would be 401 Unauthorized
        But, the 200 OK is only for the response being successful
        The failed login is returned by the success = False
    '''
    assert resp.status_code == 200 
    assert "errors" not in payload
    assert payload["data"]["login"]["success"] == False
    assert payload["data"]["login"]["user"] is None
