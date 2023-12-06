user = {
    "email": "john@simplylift.co"
}

competition = {
    "name": "Winter Classic"
}


def test_user_path(client):

    index_response = client.get('/')
    assert index_response.status_code == 200

    show_summary_response = client.post("/showSummary", data=user)

    assert show_summary_response.status_code == 200
    assert b"Welcome, john@simplylift.co" in show_summary_response.data
    assert b"Points available: 13" in show_summary_response.data

    book_response = client.get("book/Spring%20Festival/Simply%20Lift")

    assert book_response.status_code == 200
    assert b"Spring Festival" in book_response.data
    assert b"<p>Points : <strong>13</strong>, Places available: <strong>25</strong></p>" in book_response.data

    data = {"club": "Simply Lift",
            "competition": "Spring Festival",
            "places": "3"}

    purchase_response = client.post("/purchasePlaces", data=data)

    assert purchase_response.status_code == 200
    assert b"Great-booking complete! You buy 3 places !" in purchase_response.data
    assert b"Points available: 10" in purchase_response.data

    logout_response = client.get('/logout')

    assert logout_response.status_code == 302

    board_response = client.get("/board")
    assert board_response.status_code == 200
    assert b'<tr>'
    b'<th style="border: solid;">Simply Lift</th>'
    b'<th style="border: solid;">10</th>'
    b'</tr>' in board_response.data
