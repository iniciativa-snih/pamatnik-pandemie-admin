from locust import HttpUser, task, between


class Locust(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def index(self):
        self.client.get("/")
