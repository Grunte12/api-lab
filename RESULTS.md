# API lab results

## Part 0
- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401 (`{"error":"authentication failed"}`)
- Step 0.4, the name of your pizza: The Loud Quattro Stagioni
- Step 0.12, results of the three runs without a session (optional): Run 1: FAILED (401 on `/api/users/token/login`); Run 2: FAILED (401 on `/api/users/token/login`); Run 3: FAILED (401 on `/api/users/token/login`)
- Step 0.16, blocks of "how many of the three tools are excluded": 0 tools excluded (`[]`), 1 tool excluded (`["Knife"]`, `["Scissors"]`), 2 tools excluded (`["Knife", "Scissors"]`), 3 tools excluded (`["Knife", "Pizza cutter", "Scissors"]`)

## Defect report
- Title: Excluding all three tools returns HTTP 500 with an empty body instead of HTTP 400 with a JSON error message
- Request: `POST https://quickpizza.grafana.com/api/pizza` with `Authorization: token abcdef0123456789` and body `{"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}`
- Expected result: HTTP status `400` and a JSON body containing an `"error"` message explaining that no pizza can satisfy the request.
- Actual result: HTTP status `500` with `content-length: 0` and an empty response body.
- Severity: Medium (an invalid client input causes an unhandled server error and breaks JSON clients expecting an error object).

## Part A
- Step A4, status codes when the other user reads, changes and deletes:
  - Read (`GET /api/ratings/{id}`): `404` (`{"error":"not found"}`)
  - Change (`PUT /api/ratings/{id}`): `400` (`{"error":"rating ID <id> not found"}`)
  - Delete (`DELETE /api/ratings/{id}`): `400` (`{"error":"rating ID <id> not found"}`)

## Part B
1. Real API tests can find integration bugs between the HTTP layer, authentication/session middleware, and database/storage (for example, returning 500 on valid JSON input or failing sticky-session routing), as well as serialization/validation bugs (for example, wrong status codes or missing JSON error bodies). Unit tests with stubs are still worth writing because they run in milliseconds, do not need network access, and isolate logic in a single function without external flakiness.
2. Creating a fresh user per test prevents tests from colliding with each other or with other students' data on the shared server, keeping every test independent. In Project 2, each test or suite should create or isolate its own test records (carts, orders, or bookings) with unique identifiers and clean them up afterward rather than relying on shared mutable records.
3. QuickPizza runs behind an AWSALB load balancer where each backend instance holds its own in-memory users, and the `AWSALB` cookie keeps requests on the same server. Sending every request through one `requests.Session` preserves that cookie so login and follow-up calls reach the server that created the user. In Step 0.12 without a session, all three runs failed with `401` on `/api/users/token/login` because the login request was routed to a server that did not have the newly registered user.
4. The "3 tools excluded" block (`["Knife", "Pizza cutter", "Scissors"]`) revealed the defect in Step 0.16. A `500` with an empty body is worse for an API client than a `400` with a JSON error because the client cannot tell whether the request was invalid or the server crashed, and calling `.json()` on an empty body throws a parse error. Keeping the test as `xfail(strict=True)` keeps the rest of the suite green while tracking the known defect, and automatically fails the run if the server later fixes it so we know to remove the mark.
5. Base choice coverage needs `1 + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1) = 1 + 2 + 3 + 1 + 2 = 9` tests (1 base test plus one test per non-base block of C1, C2, C3, and C4). All-combinations coverage would need `3 * 4 * 2 * 3 = 72` tests.
6. The other user got `404` on `GET` and `400` on `PUT` and `DELETE`. One might expect `403 Forbidden` (or `404 Not Found` consistently across all three) when accessing another user's resource. Returning `404`/`400` instead of `403` is a common design choice to avoid leaking whether a resource ID exists, though returning `400` on `PUT`/`DELETE` while returning `404` on `GET` is slightly inconsistent rather than a major functional defect because the other user is still blocked and the rating stays unchanged.
7. Sending `Authorization: token 0000000000000000` returns `HTTP/2 200` with a JSON list of public/shared ratings instead of `401 Unauthorized`. Yes, this is a defect: the API accepts any 16-character token without verifying that it belongs to a real registered user. On a real system, a stranger could use a guessed or arbitrary 16-character token to bypass authentication and read, create, modify, or delete data without logging in.
8. An API test checks status codes, exact JSON schemas/fields, and edge-case inputs (such as invalid types or unauthorized IDs) much faster and more directly than a browser test. A test through the web pages can check visual layout, CSS rendering, client-side JavaScript behavior, and whether forms/buttons actually work for a human user on screen.
