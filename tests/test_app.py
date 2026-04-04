import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

# Helper to reset activities for test isolation
def reset_participants():
    for activity in activities.values():
        if isinstance(activity.get("participants"), list):
            activity["participants"] = []

def test_get_activities():
    # Arrange
    reset_participants()
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    # Arrange
    reset_participants()
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate():
    # Arrange
    reset_participants()
    email = "testuser@mergington.edu"
    client.post(f"/activities/Chess Club/signup?email={email}")
    # Act
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_participant():
    # Arrange
    reset_participants()
    email = "testuser@mergington.edu"
    client.post(f"/activities/Chess Club/signup?email={email}")
    # Act
    response = client.delete(f"/activities/Chess Club/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_nonexistent():
    # Arrange
    reset_participants()
    email = "notfound@mergington.edu"
    # Act
    response = client.delete(f"/activities/Chess Club/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
