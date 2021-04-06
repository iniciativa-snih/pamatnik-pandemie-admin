from locust import HttpUser, task, between


class Locust(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def index(self):
        self.client.get("/")

    @task
    def image(self):
        self.client.get("/_next/image?url=%2Fimages%2Fpersons%2Fpostava_deda2.png&w=96&q=75")
