import pytest


# Verify boundary star values (0, 1, 5, 6) when updating a rating via PUT.
@pytest.mark.parametrize(
    "stars, expected_status",
    [
        (0, 400),
        (1, 200),
        (5, 200),
        (6, 400),
    ],
)
def test_update_rating_stars_boundaries(api, auth, rating, stars, expected_status):
    res = api.put(
        f"/api/ratings/{rating['id']}",
        headers=auth,
        json={"stars": stars},
    )
    assert res.status_code == expected_status

    check = api.get(f"/api/ratings/{rating['id']}", headers=auth)
    assert check.status_code == 200
    expected_stars = stars if expected_status == 200 else 3
    assert check.json()["stars"] == expected_stars
