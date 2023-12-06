def test_point_board(client):

    response = client.get("/board")

    assert response.status_code == 200
    assert b"Point Board || GUDLFT" and b"Points" and b"Club" in response.data
