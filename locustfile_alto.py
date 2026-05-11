from locust import HttpUser, TaskSet, task, between

class TarefasAlto(TaskSet):
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

    @task
    def post_imagem_530kb(self):
        self.client.get(
            "/?p=5",
            name="Imagem 530kb (pagina)"
        )
        self.client.get(
            "/wp-content/uploads/2026/04/Captura-de-tela-2026-04-27-181334-1024x576.png",
            name="Imagem 530kb (arquivo)"
        )

class WebsiteUser(HttpUser):
    tasks = [TarefasAlto]
    wait_time = between(1, 3)