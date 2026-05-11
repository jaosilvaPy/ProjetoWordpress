from locust import HttpUser, TaskSet, task, between

# ----------------------------------------------------------------
#  CENARIO LEVE — apenas texto
# ----------------------------------------------------------------
class TarefasLeve(TaskSet):
    @task
    def post_texto_leve(self):
        self.client.get(
            "/2026/04/29/ola-mundo/",
            name="Texto leve"
        )

class UsuarioLeve(HttpUser):
    tasks = [TarefasLeve]
    wait_time = between(1, 3)


# ----------------------------------------------------------------
#  CENARIO MEDIO — texto + imagem 253kb
# ----------------------------------------------------------------
class TarefasMedio(TaskSet):
    @task
    def post_texto_leve(self):
        self.client.get(
            "/2026/04/29/ola-mundo/",
            name="Texto leve"
        )

    @task
    def post_imagem_253kb(self):
        self.client.get(
            "/2026/05/04/image-250kb/",
            name="Imagem 253kb (pagina)"
        )
        self.client.get(
            "/wp-content/uploads/2026/05/FotoJaoeAnaCastelao_11zon_11zon-1-683x1024.jpg",
            name="Imagem 253kb (arquivo)"
        )

class UsuarioMedio(HttpUser):
    tasks = [TarefasMedio]
    wait_time = between(1, 3)


# ----------------------------------------------------------------
#  CENARIO ALTO — texto + imagem 253kb + imagem 530kb
# ----------------------------------------------------------------
class TarefasAlto(TaskSet):
    @task
    def post_texto_leve(self):
        self.client.get(
            "/2026/04/29/ola-mundo/",
            name="Texto leve"
        )

    @task
    def post_imagem_253kb(self):
        self.client.get(
            "/2026/05/04/image-250kb/",
            name="Imagem 253kb (pagina)"
        )
        self.client.get(
            "/wp-content/uploads/2026/05/FotoJaoeAnaCastelao_11zon_11zon-1-683x1024.jpg",
            name="Imagem 253kb (arquivo)"
        )

    @task
    def post_imagem_530kb(self):
        self.client.get(
            "/2026/04/29/post530kb/",
            name="Imagem 530kb (pagina)"
        )
        self.client.get(
            "/wp-content/uploads/2026/04/Captura-de-tela-2026-04-27-181334-1024x576.png",
            name="Imagem 530kb (arquivo)"
        )

class UsuarioAlto(HttpUser):
    tasks = [TarefasAlto]
    wait_time = between(1, 3)