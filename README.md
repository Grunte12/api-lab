# QuickPizza API Tests

API tests for `https://quickpizza.grafana.com` using `pytest` and `requests`.

## Setup and Run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pytest -v
```

To generate the HTML report:

```bash
.venv/bin/pytest -v --html=report.html --self-contained-html
```

## Input Domain Model for `POST /api/ratings` (Step A1 & A2)

Base choice: `stars=3`, existing `pizza_id`, logged-in user `Authorization` header.

| Characteristic | Block | Value(s) | Expected Status | Covering Test |
| --- | --- | --- | --- | --- |
| C1: `stars` range | Valid (base) | `3` | `201` | `test_create_rating_base_choice` |
| C1: `stars` range | Below min | `0` | `400` | `test_stars_out_of_range[0]` |
| C1: `stars` range | Above max | `6` | `400` | `test_stars_out_of_range[6]` |
| C2: `stars` type/presence | Decimal | `3.5` | `400` | `test_stars_invalid_type_or_missing[decimal]` |
| C2: `stars` type/presence | String | `"3"` | `400` | `test_stars_invalid_type_or_missing[text]` |
| C2: `stars` type/presence | Missing field | *(omitted)* | `400` | `test_stars_invalid_type_or_missing[missing]` |
| C3: `pizza_id` existence | Existing (base) | `pizza_id` fixture | `201` | `test_create_rating_base_choice` |
| C3: `pizza_id` existence | Non-existent | `999999999` | `400` | `test_unknown_pizza_id_refused` |
| C4: `Authorization` header | Valid token (base) | `auth` fixture | `201` | `test_create_rating_base_choice` |
| C4: `Authorization` header | No header | `{}` | `401` | `test_create_rating_invalid_auth[no_header]` |
| C4: `Authorization` header | Invalid/short token | `token short` | `401` | `test_create_rating_invalid_auth[short_token]` |
