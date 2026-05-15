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
    "leve":  "Texto Leve",
    "medio": "Imagem 253kb",
    "alto":  "Imagem 500kb",
}

NOMES_ARQ = {
    "1inst": "1 Instância",
    "2inst": "2 Instâncias",
    "3inst": "3 Instâncias",
}

CORES = {
    "1inst": "#E74C3C",
    "2inst": "#F39C12",
    "3inst": "#27AE60",
}

CORES_CARGA = {
    "100": "#3498DB",
    "200": "#9B59B6",
    "350": "#E67E22",
}


# ---------------------------------------------------------------
def ler_stats(arq, cenario, carga):
    mapear_carga = {"100": "baixa", "200": "media", "350": "alta"}
    nome_carga = mapear_carga.get(carga)
    nome_arquivo = f"resultado_{cenario}_{nome_carga}_stats.csv"
    path = os.path.join(RESULTADOS, arq, nome_arquivo)

    if not os.path.exists(path):
        print(f"  Aviso: não encontrado -> {path}")
        return None

    try:
        df = pd.read_csv(path)
        row = df[df["Name"] == "Aggregated"]
        return row.iloc[0] if not row.empty else None
    except Exception as e:
        print(f"  Erro ao ler {nome_arquivo}: {e}")
        return None


def salvar(fig, nome):
    path = os.path.join(GRAFICOS, nome)
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  Salvo: {path}")


# ---------------------------------------------------------------
# BLOCO A — Eixo X = Número de Usuários  |  Linhas = Instâncias
#           Cada instância: linha sólida (Média) + linha tracejada (P95)
# ---------------------------------------------------------------
print("\n[A] TEMPO DE RESPOSTA vs USUÁRIOS (Média + P95) — linha por instância")

for cenario in CENARIOS:
    fig, ax = plt.subplots(figsize=(10, 5.5))

    for arq in ARQUITETURAS:
        x_vals, y_avg, y_p95 = [], [], []

        for carga in CARGAS:
            r = ler_stats(arq, cenario, carga)
            if r is not None:
                x_vals.append(int(carga))
                y_avg.append(r["Average Response Time"])
                # Coluna P95 nos CSVs do Locust chama-se "95%"
                p95_val = r.get("95%", None)
                y_p95.append(p95_val if p95_val is not None else float("nan"))

        if x_vals:
            cor = CORES[arq]
            label = NOMES_ARQ[arq]
            ax.plot(x_vals, y_avg,
                    marker="o", color=cor, linewidth=2,
                    label=f"{label} — Média")
            ax.plot(x_vals, y_p95,
                    marker="s", color=cor, linewidth=2,
                    linestyle="--",
                    label=f"{label} — P95")

    ax.set_title(
        f"Tempo de Resposta vs Usuários — {NOMES_CENARIO[cenario]}",
        fontsize=13, fontweight="bold")
    ax.set_xlabel("Número de Usuários", fontsize=11)
    ax.set_ylabel("Tempo de Resposta (ms)", fontsize=11)
    ax.set_xticks([100, 200, 350])
    ax.legend(fontsize=9, ncol=2)
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    salvar(fig, f"A_tempo_vs_usuarios_{cenario}.png")


# ---------------------------------------------------------------
# BLOCO B — Eixo X = Número de Instâncias  |  Linhas = Cargas
#           Cada carga: linha sólida (Média) + linha tracejada (P95)
# ---------------------------------------------------------------
print("\n[B] TEMPO DE RESPOSTA vs INSTÂNCIAS (Média + P95) — linha por carga")

x_inst = [1, 2, 3]

for cenario in CENARIOS:
    fig, ax = plt.subplots(figsize=(10, 5.5))

    for carga in CARGAS:
        y_avg, y_p95 = [], []

        for arq in ARQUITETURAS:
            r = ler_stats(arq, cenario, carga)
            if r is not None:
                y_avg.append(r["Average Response Time"])
                p95_val = r.get("95%", None)
                y_p95.append(p95_val if p95_val is not None else float("nan"))
            else:
                y_avg.append(None)
                y_p95.append(None)

        # filtra None mantendo alinhamento com x_inst
        x_a, ya_c, yp_c = zip(*[
            (x_inst[i], y_avg[i], y_p95[i])
            for i in range(3)
            if y_avg[i] is not None
        ]) if any(v is not None for v in y_avg) else ([], [], [])

        if x_a:
            cor = CORES_CARGA[carga]
            label = f"{carga} usuários"
            ax.plot(x_a, ya_c,
                    marker="o", color=cor, linewidth=2,
                    label=f"{label} — Média")
            ax.plot(x_a, yp_c,
                    marker="s", color=cor, linewidth=2,
                    linestyle="--",
                    label=f"{label} — P95")

    ax.set_title(
        f"Tempo de Resposta vs Instâncias — {NOMES_CENARIO[cenario]}",
        fontsize=13, fontweight="bold")
    ax.set_xlabel("Número de Instâncias WordPress", fontsize=11)
    ax.set_ylabel("Tempo de Resposta (ms)", fontsize=11)
    ax.set_xticks([1, 2, 3])
    ax.legend(fontsize=9, ncol=2)
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    salvar(fig, f"B_tempo_vs_instancias_{cenario}.png")


# ---------------------------------------------------------------
# BLOCO C — RPS vs Usuários  |  Linhas = Instâncias
# ---------------------------------------------------------------
print("\n[C] RPS vs USUÁRIOS — linha por instância")

for cenario in CENARIOS:
    fig, ax = plt.subplots(figsize=(10, 5.5))

    for arq in ARQUITETURAS:
        x_vals, y_rps = [], []
        for carga in CARGAS:
            r = ler_stats(arq, cenario, carga)
            if r is not None:
                x_vals.append(int(carga))
                y_rps.append(r["Requests/s"])
        if x_vals:
            ax.plot(x_vals, y_rps,
                    marker="o", color=CORES[arq], linewidth=2,
                    label=NOMES_ARQ[arq])

    ax.set_title(
        f"Requisições por Segundo vs Usuários — {NOMES_CENARIO[cenario]}",
        fontsize=13, fontweight="bold")
    ax.set_xlabel("Número de Usuários", fontsize=11)
    ax.set_ylabel("Requisições por Segundo", fontsize=11)
    ax.set_xticks([100, 200, 350])
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    salvar(fig, f"C_rps_vs_usuarios_{cenario}.png")


# ---------------------------------------------------------------
# BLOCO D — RPS vs Instâncias  |  Linhas = Cargas
# ---------------------------------------------------------------
print("\n[D] RPS vs INSTÂNCIAS — linha por carga")

for cenario in CENARIOS:
    fig, ax = plt.subplots(figsize=(10, 5.5))

    for carga in CARGAS:
        y_rps = []
        for arq in ARQUITETURAS:
            r = ler_stats(arq, cenario, carga)
            y_rps.append(r["Requests/s"] if r is not None else None)

        x_c, y_c = zip(*[
            (x_inst[i], y_rps[i])
            for i in range(3)
            if y_rps[i] is not None
        ]) if any(v is not None for v in y_rps) else ([], [])

        if x_c:
            ax.plot(x_c, y_c,
                    marker="o", color=CORES_CARGA[carga], linewidth=2,
                    label=f"{carga} usuários")

    ax.set_title(
        f"RPS vs Instâncias — {NOMES_CENARIO[cenario]}",
        fontsize=13, fontweight="bold")
    ax.set_xlabel("Número de Instâncias WordPress", fontsize=11)
    ax.set_ylabel("Requisições por Segundo", fontsize=11)
    ax.set_xticks([1, 2, 3])
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    salvar(fig, f"D_rps_vs_instancias_{cenario}.png")


# ---------------------------------------------------------------
# BLOCO E — Taxa de Falhas vs Usuários  |  Linhas = Instâncias
# ---------------------------------------------------------------
print("\n[E] TAXA DE FALHAS vs USUÁRIOS — linha por instância")

for cenario in CENARIOS:
    fig, ax = plt.subplots(figsize=(10, 5.5))

    for arq in ARQUITETURAS:
        x_vals, y_pct = [], []
        for carga in CARGAS:
            r = ler_stats(arq, cenario, carga)
            if r is not None:
                reqs = r["Request Count"]
                falhas = r["Failure Count"]
                pct = (falhas / reqs * 100) if reqs > 0 else 0
                x_vals.append(int(carga))
                y_pct.append(pct)
        if x_vals:
            ax.plot(x_vals, y_pct,
                    marker="^", color=CORES[arq], linewidth=2,
                    label=NOMES_ARQ[arq])

    ax.set_title(
        f"Taxa de Falhas vs Usuários — {NOMES_CENARIO[cenario]}",
        fontsize=13, fontweight="bold")
    ax.set_xlabel("Número de Usuários", fontsize=11)
    ax.set_ylabel("Falhas (%)", fontsize=11)
    ax.set_xticks([100, 200, 350])
    ax.set_ylim(0, 100)
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    salvar(fig, f"E_falhas_vs_usuarios_{cenario}.png")


# ---------------------------------------------------------------
print(f"\n TODOS OS GRÁFICOS SALVOS EM {GRAFICOS}/")
print(f" TOTAL: {len(os.listdir(GRAFICOS))} arquivos")
