from urllib.parse import quote


def test_get_activities(client):
    # Arrange: client fixture provided

    # Act
    resp = client.get("/activities")
    data = resp.json()

    # Assert: Basic sanity checks
    assert resp.status_code == 200
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_adds_participant(client):
    # Arrange
    activity = "Basketball Club"
    email = "alice.test@mergington.edu"
    data = client.get("/activities").json()
    assert email not in data[activity]["participants"]

    # Act
    resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    data = client.get("/activities").json()
    assert email in data[activity]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity = "Programming Class"
    email = "dup.user@mergington.edu"

    # Act
    r1 = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    r2 = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert r1.status_code == 200
    assert r2.status_code == 400


def test_unregister_removes_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    data = client.get("/activities").json()
    assert email in data[activity]["participants"]

    # Act
    r = client.delete(f"/activities/{quote(activity)}/participants", params={"email": email})

    # Assert
    assert r.status_code == 200
    assert "Unregistered" in r.json().get("message", "")

    data = client.get("/activities").json()
    assert email not in data[activity]["participants"]


def test_unregister_nonexistent_returns_404(client):
    # Arrange
    activity = "Science Club"
    email = "notfound@mergington.edu"

    # Act
    r = client.delete(f"/activities/{quote(activity)}/participants", params={"email": email})

    # Assert
    assert r.status_code == 404


def test_activity_not_found_returns_404(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "someone@mergington.edu"

    # Act
    r1 = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    r2 = client.delete(f"/activities/{quote(activity)}/participants", params={"email": email})

    # Assert
    assert r1.status_code == 404
    assert r2.status_code == 404

