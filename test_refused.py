import uuid


# Verify that registering with a duplicate username is refused with 400.
def test_duplicate_username_refused(api):
    name = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": name, "password": "Pizza-2026"}
    first = api.post("/api/users", json=user)
    assert first.status_code == 201

    second = api.post("/api/users", json=user)
    assert second.status_code == 400
    assert second.json()["error"] == "username already taken"


# Verify that logging in with a wrong password is refused with 401.
def test_wrong_password_refused(api):
    name = "lab-" + uuid.uuid4().hex[:12]
    res = api.post("/api/users", json={"username": name, "password": "Pizza-2026"})
    assert res.status_code == 201

    login = api.post(
        "/api/users/token/login",
        json={"username": name, "password": "wrong-password"},
    )
    assert login.status_code == 401
    assert login.json()["error"] == "authentication failed"


# Verify that registering with an empty username is refused with 400.
def test_empty_username_refused(api):
    res = api.post("/api/users", json={"username": "", "password": "Pizza-2026"})
    assert res.status_code == 400
    assert res.json()["error"] == "username field is empty"
