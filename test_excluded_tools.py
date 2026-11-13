import pytest


# Verify that excluding 0, 1, or 2 tools still returns a pizza using an allowed tool.
@pytest.mark.parametrize(
    "excluded",
    [
        [],
        ["Knife"],
        ["Scissors"],
        ["Knife", "Scissors"],
    ],
)
def test_excluded_tools(api, excluded):
    res = api.post(
        "/api/pizza",
        headers={"Authorization": "token abcdef0123456789"},
        json={"excludedTools": excluded},
    )
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded


# Verify that excluding all three tools is refused with 400 and a JSON error message.
@pytest.mark.xfail(
    reason="Defect 1: excluding all three tools returns 500 with empty body instead of 400 with JSON error",
    strict=True,
)
def test_exclude_all_tools_refused(api):
    res = api.post(
        "/api/pizza",
        headers={"Authorization": "token abcdef0123456789"},
        json={"excludedTools": ["Knife", "Pizza cutter", "Scissors"]},
    )
    assert res.status_code == 400
    assert "error" in res.json()
