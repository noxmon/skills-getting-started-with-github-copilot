from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore the in-memory activity data before and after each test."""
    # Arrange
    original_data = deepcopy(app_module.activities)
    app_module.activities = deepcopy(original_data)

    yield

    # Arrange
    app_module.activities = original_data


@pytest.fixture()
def client():
    """Create a test client for the FastAPI app."""
    # Arrange
    with TestClient(app_module.app) as test_client:
        yield test_client


def test_root_redirects_to_static_index(client):
    # Arrange

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_seed_data(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["max_participants"] == 12
    assert "michael@mergington.edu" in payload["Chess Club"]["participants"]


def test_signup_for_activity_adds_student(client):
    # Arrange
    activity_name = "Chess Club"
    student_email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {student_email} for {activity_name}"
    assert student_email in app_module.activities[activity_name]["participants"]
