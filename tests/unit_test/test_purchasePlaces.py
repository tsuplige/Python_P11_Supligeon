def test_purchase_places_with_enough_point(client):
    data = {"club": "Simply Lift",
            "competition": "Spring Festival",
            "places": "3"}
    response = client.post("/purchasePlaces", data=data)

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data


def test_purchase_places_without_enough_point(client):
    data = {"club": "Iron Temple",
            "competition": "Spring Festival",
            "places": "6"}
    response = client.post("/purchasePlaces", data=data)

    assert response.status_code == 403
    assert b"The club does not have enough points to order" in response.data


def test_purchase_more_than_12_places(client):
    data = {"club": "Simply Lift",
            "competition": "Spring Festival",
            "places": "13"}
    response = client.post("/purchasePlaces", data=data)

    assert response.status_code == 403
    assert b"you cannot purchase more than 12 places" in response.data


def test_purchase_places_with_inexistant_club(client):
    data = {"club": "Cobra kai",
            "competition": "Spring Festival",
            "places": "3"}
    response = client.post("/purchasePlaces", data=data)

    assert response.status_code == 404
    assert b"The club does not exist in database" in response.data


def test_purchase_places_for_inexistant_competition(client):
    data = {"club": "Simply Lift",
            "competition": "Tenkaichi Budokai",
            "places": "3"}
    response = client.post("/purchasePlaces", data=data)

    assert response.status_code == 404
    assert b"The competition does not exist in database" in response.data


def test_purchase_places_more_than_available(client):
    data = {"club": "Simply Lift",
            "competition": "Winter Classic",
            "places": "8"}
    response = client.post("/purchasePlaces", data=data)

    assert response.status_code == 403
    assert (b"You cannot purchase more than the available places"
            in response.data)


def test_purchase_places_without_place_spécified(client):
    data = {"club": "Simply Lift",
            "competition": "Winter Classic",
            "places": ""}
    response = client.post("/purchasePlaces", data=data)

    assert response.status_code == 400
    assert b"number places not specified" in response.data
