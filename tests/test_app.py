from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    activity_name = "Programming Class"
    email = "newstudent@mergington.edu"

    first_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    second_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_email():
    activity_name = "Programming Class"
    email = "unregisterstudent@mergington.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    delete_response = client.delete(
        f"/activities/{activity_name}/signup?email={email}"
    )

    assert signup_response.status_code == 200
    assert delete_response.status_code == 200
    assert delete_response.json()["detail"] == f"Removed {email} from {activity_name}"
