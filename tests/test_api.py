import copy
from urllib.parse import quote


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Basic sanity checks
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_adds_participant(client):
    activity = "Basketball Club"
    email = "alice.test@mergington.edu"

    # Ensure participant not present initially
    data = client.get("/activities").json()
    assert email not in data[activity]["participants"]

    # Sign up
    resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify participant is present
    data = client.get("/activities").json()
    assert email in data[activity]["participants"]


def test_signup_duplicate_returns_400(client):
    activity = "Programming Class"
    email = "dup.user@mergington.edu"

    # First signup should succeed
    r1 = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert r1.status_code == 200

    # Second signup should return 400
    r2 = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert r2.status_code == 400


def test_unregister_removes_participant(client):
    activity = "Chess Club"
    # Use an existing participant from the initial dataset
    email = "michael@mergington.edu"

    # Ensure participant exists
    data = client.get("/activities").json()
    assert email in data[activity]["participants"]

    # Unregister
    r = client.delete(f"/activities/{quote(activity)}/participants", params={"email": email})
    assert r.status_code == 200
    assert "Unregistered" in r.json().get("message", "")

    # Verify removal
    data = client.get("/activities").json()
    assert email not in data[activity]["participants"]


def test_unregister_nonexistent_returns_404(client):
    activity = "Science Club"
    email = "notfound@mergington.edu"

    r = client.delete(f"/activities/{quote(activity)}/participants", params={"email": email})
    assert r.status_code == 404


def test_activity_not_found_returns_404(client):
    activity = "Nonexistent Club"
    email = "someone@mergington.edu"

    r1 = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert r1.status_code == 404

    r2 = client.delete(f"/activities/{quote(activity)}/participants", params={"email": email})
    assert r2.status_code == 404

