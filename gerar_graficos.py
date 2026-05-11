import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

RESULTADOS = "./resultados"
GRAFICOS = "./graficos"

os.makedirs(GRAFICOS, exist_ok=True)

ARQUITETURAS = ["1inst", "2inst", "3inst"]
CENARIOS = ["leve", "medio", "alto"]
CARGAS = ["100", "200", "350"]

NOMES_CENARIO = {
    "leve": "Texto Leve",
    "medio": "Imagem 253kb",
    "alto": "Imagem 500kb",
}

NOMES_ARQ = {
    "1inst": "1 Instancia",
    "2inst": "2 Instancias",
    "3inst": "3 Instancias",
}

CORES = {
    "1inst": "#E74C3C",
    "2inst": "#F39C12",
    "3inst": "#27AE60",
}


def ler_stats(arq, cenario, carga):
    # Mapeia o numero da carga
    mapear_carga = {"100": "baixa", "200": "media", "350": "alta"}
    nome_carga = mapear_carga.get(carga)

    # O nome do arquivo
    nome_arquivo = f"resultado_{cenario}_{nome_carga}_stats.csv"

    path = os.path.join(RESULTADOS, arq, nome_arquivo)

    if not os.path.exists(path):
        print(f"Aviso: Arquivo não encontrado -> {path}")
        return None

    try:
        df = pd.read_csv(path)
        row = df[df["Name"] == "Aggregated"]
        if row.empty:
            return None
        return row.iloc[0]
    except Exception as e:
        print(f"Erro ao ler {nome_arquivo}: {e}")
        return None


def salvar(fig, nome):
    path = os.path.join(GRAFICOS, nome)
    fig.savefig(path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Salvo: {path}")


print("\n [1] TEMPO DE RESPOSTA MÉDIO POR NÚMERO DE USUÁRIOS")
for cenario in CENARIOS:
    fig, ax = plt.subplots(figsize=(9, 5))
    for arq in ARQUITETURAS:
        y = []
        x = []
        for carga in CARGAS:
            r = ler_stats(arq, cenario, carga)
            if r is not None:
                x.append(int(carga))
                y.append(r["Average Response Time"])
        if x:
            ax.plot(x, y, marker="o",
                    label=NOMES_ARQ[arq],
                    color=CORES[arq],
                    linewidth=2)

    ax.set_title(
        f"Tempo de Resposta Médio - {NOMES_CENARIO[cenario]}", fontsize=13, fontweight="bold")
    ax.set_xlabel("Número de Usuários", fontsize=11)
    ax.set_ylabel("Tempo de Resposta Médio (ms)", fontsize=11)
    ax.set_xticks([100, 200, 350])
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    fig.tight_layout()
    salvar(fig, f"tempo_resposta_medio_{cenario}.png")


print("\n [2] REQUISIÇÕES POR SEGUNDO POR NUMERO DE USUARIOS")
for cenario in CENARIOS:
    fig, ax = plt.subplots(figsize=(9, 5))
    for arq in ARQUITETURAS:
        y = []
        x = []
        for carga in CARGAS:
            r = ler_stats(arq, cenario, carga)
            if r is not None:
                x.append(int(carga))
                y.append(r["Requests/s"])
        if x:
            ax.plot(x, y, marker="o",
                    label=NOMES_ARQ[arq],
                    color=CORES[arq],
                    linewidth=2)
    ax.set_title(
        f"Requisições por Segundo - {NOMES_CENARIO[cenario]}", fontsize=13, fontweight="bold")
    ax.set_xlabel("Número de Usuários", fontsize=11)
    ax.set_ylabel("Requisições por Segundo", fontsize=11)
    ax.set_xticks([100, 200, 350])
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    fig.tight_layout()
    salvar(fig, f"requisicoes_por_segundo_{cenario}.png")


print("\n [3] TAXA DE FALHAS POR NÚMERO DE USUÁRIOS")
for cenario in CENARIOS:
    fig, ax = plt.subplots(figsize=(9, 5))
    for arq in ARQUITETURAS:
        y = []
        x = []
        for carga in CARGAS:
            r = ler_stats(arq, cenario, carga)
            if r is not None:
                reqs = r["Request Count"]
                falhas = r["Failure Count"]
                pct = (falhas / reqs * 100) if reqs > 0 else 0
                x.append(int(carga))
                y.append(pct)
        if x:
            ax.plot(x, y, marker="^",
                    label=NOMES_ARQ[arq],
                    color=CORES[arq],
                    linewidth=2)

    ax.set_title(
        f"Taxa de Falhas - {NOMES_CENARIO[cenario]}", fontsize=13, fontweight="bold")
    ax.set_xlabel("Número de Usuários", fontsize=11)
    ax.set_ylabel("Falhas (%)", fontsize=11)
    ax.set_xticks([100, 200, 350])
    ax.set_ylim(0, 100)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    fig.tight_layout()
    salvar(fig, f"falhas_{cenario}.png")

print("\n [4] TEMPO DE RESPOSTA POR NUMERO DE INSTANCIAS")

x_inst = [1, 2, 3]

for cenario in CENARIOS:
    fig, ax = plt.subplots(figsize=(9, 5))

    for carga in CARGAS:
        y = []

        for arq in ARQUITETURAS:
            r = ler_stats(arq, cenario, carga)

            if r is not None:
                y.append(r["Average Response Time"])
            else:
                y.append(None)

        y_clean = [v for v in y if v is not None]
        x_clean = [x_inst[i] for i, v in enumerate(y) if v is not None]

        if x_clean:
            ax.plot(
                x_clean,
                y_clean,
                marker="o",
                label=f"{carga} usuarios",
                linewidth=2
            )

    ax.set_title(
        f"Tempo de Resposta Médio por Número de Instâncias - {NOMES_CENARIO[cenario]}",
        fontsize=13,
        fontweight="bold"
    )

    ax.set_xlabel("Número de Instâncias", fontsize=11)
    ax.set_ylabel("Tempo de Resposta Médio (ms)", fontsize=11)

    ax.set_xticks([1, 2, 3])

    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)

    fig.tight_layout()

    salvar(fig, f"tempo_por_instancias_{cenario}.png")

print("\n [5] RPS por numero de instancias")

for cenario in CENARIOS:
    fig, ax = plt.subplots(figsize=(9, 5))

    for carga in CARGAS:
        y = []

        for arq in ARQUITETURAS:
            r = ler_stats(arq, cenario, carga)

            if r is not None:
                y.append(r["Requests/s"])
            else:
                y.append(None)

        y_clean = [v for v in y if v is not None]
        x_clean = [x_inst[i] for i, v in enumerate(y) if v is not None]

        if x_clean:
            ax.plot(
                x_clean,
                y_clean,
                marker="o",
                label=f"{carga} usuarios",
                linewidth=2
            )

    ax.set_title(
        f"RPS por Instâncias - {NOMES_CENARIO[cenario]}",
        fontsize=13,
        fontweight="bold"
    )

    ax.set_xlabel("Número de Instâncias Wordpress", fontsize=11)
    ax.set_ylabel("Requests/s", fontsize=11)

    ax.set_xticks([1, 2, 3])

    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)

    fig.tight_layout()

    salvar(fig, f"rps_por_instancias_{cenario}.png")

print(f"\n TODOS OS GRÁFICOS SALVOS EM {GRAFICOS}")
print(f"TOTAL: {len(os.listdir(GRAFICOS))} arquivos")
