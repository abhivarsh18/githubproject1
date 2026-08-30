from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from src.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_duplicate_signup_is_rejected(client):
    # Arrange
    activity_name = "Programming Class"
    email = f"{uuid4()}@mergington.edu"

    # Act
    first_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    second_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_email(client):
    # Arrange
    activity_name = "Programming Class"
    email = f"{uuid4()}@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    delete_response = client.delete(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert signup_response.status_code == 200
    assert delete_response.status_code == 200
    assert delete_response.json()["detail"] == f"Removed {email} from {activity_name}"
