# Verify that another user cannot read a rating they do not own.
def test_other_user_cannot_read_rating(api, auth, other_auth, rating):
    res = api.get(f"/api/ratings/{rating['id']}", headers=other_auth)
    assert res.status_code in range(400, 500)

    check = api.get(f"/api/ratings/{rating['id']}", headers=auth)
    assert check.status_code == 200
    assert check.json()["stars"] == 3


# Verify that another user cannot update a rating they do not own.
def test_other_user_cannot_update_rating(api, auth, other_auth, rating):
    res = api.put(
        f"/api/ratings/{rating['id']}",
        headers=other_auth,
        json={"stars": 1},
    )
    assert res.status_code in range(400, 500)

    check = api.get(f"/api/ratings/{rating['id']}", headers=auth)
    assert check.status_code == 200
    assert check.json()["stars"] == 3


# Verify that another user cannot delete a rating they do not own.
def test_other_user_cannot_delete_rating(api, auth, other_auth, rating):
    res = api.delete(f"/api/ratings/{rating['id']}", headers=other_auth)
    assert res.status_code in range(400, 500)

    check = api.get(f"/api/ratings/{rating['id']}", headers=auth)
    assert check.status_code == 200
    assert check.json()["stars"] == 3
