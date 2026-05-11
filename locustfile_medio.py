from locust import HttpUser, TaskSet, task, between

class TarefasMedio(TaskSet):
    @task
    def post_texto_leve(self):
        self.client.get(
            "/?p=1",
            name="Texto leve"
        )

    @task
    def post_imagem_253kb(self):
        self.client.get(
            "/?p=13",
            name="Imagem 253kb (pagina)"
        )
        self.client.get(
            "/wp-content/uploads/2026/05/FotoJaoeAnaCastelao_11zon_11zon-1-683x1024.jpg",
            name="Imagem 253kb (arquivo)"
        )

class WebsiteUser(HttpUser):
    tasks = [TarefasMedio]
    wait_time = between(1, 3)