def test_book_with_correct_link(client):

    response = client.get('/book/Winter%20Classic/Simply%20Lift')

    assert b"you can purchase" and b"Winter Classic" in response.data
    assert response.status_code == 200


def test_book_with_bad_link(client):

    response = client.get('/book/Unknow%20Competition/Unknow%20Club')
    assert b"Something went wrong-please try again" in response.data
    assert response.status_code == 404


def test_book_with_empty_link(client):

    response = client.get('/book')

    assert response.status_code == 404
