
def test_show_summary_with_unregistered_mail(client):

    data = {
        "email": "test@email.te",
        }
    response = client.post("/showSummary", data=data)

    assert response.status_code == 404
    assert b"like the email isn&#39;t found" in response.data


def test_show_summary_with_registered_mail(client):

    data = {
        "email": "admin@irontemple.com",
        }
    response = client.post("/showSummary", data=data)

    assert response.status_code == 200
    assert b"Summary | GUDLFT Registration" in response.data
