def register_and_login(
    client,
):

    email = (
        "tester@example.com"
    )


    response = client.post(
        "/api/auth/register",

        json={
            "name": "Test User",
            "email": email,
            "password": "password123",
        },
    )


    assert response.status_code == 200


    response = client.post(
        "/api/auth/login",

        json={
            "email": email,
            "password": "password123",
        },
    )


    assert response.status_code == 200


def test_health(
    client,
):

    response = client.get(
        "/api/health"
    )


    assert response.status_code == 200


    assert (
        response.json()["status"]
        == "ok"
    )


def test_auth(
    client,
):

    register_and_login(
        client
    )


    response = client.get(
        "/api/auth/me"
    )


    assert response.status_code == 200


    assert (
        response.json()["user"]["email"]
        == "tester@example.com"
    )


def test_home_recommendation(
    client,
):

    register_and_login(
        client
    )


    response = client.post(
        "/api/generate-home",

        json={
            "budget": 100000,

            "style": "Modern",

            "rooms": [
                "Living Room",
                "Bedroom",
            ],

            "quantities": {},
        },
    )


    assert response.status_code == 200


    data = response.json()


    assert (
        data["planner"]
        == "home"
    )


    assert data[
        "recommendations"
    ]


    assert data[
        "history_id"
    ]


def test_party_recommendation(
    client,
):

    register_and_login(
        client
    )


    response = client.post(
        "/api/generate-party",

        json={
            "budget": 50000,

            "guests": 50,

            "event_type": "Birthday",

            "venue_preference":
                "Flexible",

            "city": "Chennai",
        },
    )


    assert response.status_code == 200


    assert (
        response.json()["planner"]
        == "party"
    )


def test_history(
    client,
):

    register_and_login(
        client
    )


    client.post(
        "/api/generate-home",

        json={
            "budget": 50000,

            "style": "Minimal",

            "rooms": [
                "Bedroom"
            ],

            "quantities": {},
        },
    )


    response = client.get(
        "/api/history"
    )


    assert response.status_code == 200


    assert (
        len(
            response.json()["items"]
        )
        == 1
    )