
from locust import HttpUser, TaskSet, task, between

class TarefasLeve(TaskSet):
    @task
    def post_texto_leve(self):
        self.client.get(
            "/?p=1",
            name="Texto leve"
        )

class WebsiteUser(HttpUser):
    tasks = [TarefasLeve]
    wait_time = between(1, 3)