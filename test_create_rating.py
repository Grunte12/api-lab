import pytest


# Verify the base choice for creating a rating returns 201 with the saved rating.
def test_create_rating_base_choice(api, auth, pizza_id):
    res = api.post(
        "/api/ratings",
        headers=auth,
        json={"pizza_id": pizza_id, "stars": 3},
    )
    assert res.status_code == 201
    body = res.json()
    assert body["stars"] == 3
    assert body["pizza_id"] == pizza_id


# Verify that out-of-range star counts (0 and 6) are refused with 400.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    res = api.post(
        "/api/ratings",
        headers=auth,
        json={"pizza_id": pizza_id, "stars": stars},
    )
    assert res.status_code == 400
    assert res.json()["error"] == "number of stars must be between 1 and 5 (inclusive)"


# Verify that non-integer or missing stars fields are refused with 400.
@pytest.mark.parametrize(
    "payload",
    [
        {"stars": 3.5},
        {"stars": "3"},
        {},
    ],
    ids=["decimal", "text", "missing"],
)
def test_stars_invalid_type_or_missing(api, auth, pizza_id, payload):
    body = {"pizza_id": pizza_id, **payload}
    res = api.post("/api/ratings", headers=auth, json=body)
    assert res.status_code == 400
    assert "error" in res.json()


# Verify that rating a non-existent pizza_id is refused with 400.
def test_unknown_pizza_id_refused(api, auth):
    res = api.post(
        "/api/ratings",
        headers=auth,
        json={"pizza_id": 999999999, "stars": 3},
    )
    assert res.status_code == 400
    assert res.json()["error"] == "pizza ID 999999999 not found"


# Verify that creating a rating without a valid auth token is refused with 401.
@pytest.mark.parametrize(
    "headers",
    [
        {},
        {"Authorization": "token short"},
    ],
    ids=["no_header", "short_token"],
)
def test_create_rating_invalid_auth(api, pizza_id, headers):
    res = api.post(
        "/api/ratings",
        headers=headers,
        json={"pizza_id": pizza_id, "stars": 3},
    )
    assert res.status_code == 401
    assert res.json()["error"] == "authentication failed"
