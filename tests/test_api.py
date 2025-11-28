from fastapi.testclient import TestClient
import pytest

from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    # choose an activity and a test email
    activity = "Test Club"
    email = "tester@example.com"

    # ensure activity exists in-memory for test isolation
    activities.setdefault(activity, {
        "description": "Temp activity",
        "schedule": "Now",
        "max_participants": 5,
        "participants": []
    })

    # signup
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # duplicate signup should error
    resp_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_dup.status_code == 400

    # unregister
    resp_un = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp_un.status_code == 200
    assert email not in activities[activity]["participants"]

    # unregister again should return 404
    resp_un2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp_un2.status_code == 404
