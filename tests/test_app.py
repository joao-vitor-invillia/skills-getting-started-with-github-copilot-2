from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_unregister_participant_from_activity():
    activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]

    response = client.delete(
        "/activities/Chess%20Club/unregister?email=daniel@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered daniel@mergington.edu from Chess Club"
    }
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_missing_participant_returns_error():
    activities["Basketball Team"]["participants"] = ["alex@mergington.edu"]

    response = client.delete(
        "/activities/Basketball%20Team/unregister?email=notregistered@mergington.edu"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not registered for this activity"
