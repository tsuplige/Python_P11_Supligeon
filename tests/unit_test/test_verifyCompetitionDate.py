from server import verifyCompetitionDate


def test_verify_competition_date_with_future_date(client):

    data = "2024-10-22 13:30:00"

    assert verifyCompetitionDate(data) == True


def test_verify_competition_date_with_past_date(client):

    data = "2020-10-22 13:30:00"

    assert verifyCompetitionDate(data) == False


def test_verify_competition_date_with_wrong_data(client):

    data = "Test"

    assert verifyCompetitionDate(data) == False
