from locust import HttpUser, task


class ProjectPerfTest(HttpUser):

    @task
    def index(self):
        self.client.get('')

    @task
    def display_board(self):
        self.client.get('board')

    @task
    def purchase_places(self):
        self.client.post('purchasePlaces', data={"club": "Simply Lift",
                                                 "competition": "Spring Festival",
                                                 "places": 1})
