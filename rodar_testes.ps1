# ----------------------------------------------------------------
#  DEFINA A ARQUITETURA ANTES DE RODAR: "1inst", "2inst" ou "3inst"
# ----------------------------------------------------------------
$ARQUITETURA = "1inst"

$TEMPO_TESTE = "90s"

$CARGAS = @(
    @{ nome = "baixa"; users = 100; rate = 5  },
    @{ nome = "media"; users = 350; rate = 15 },
    @{ nome = "alta";  users = 500; rate = 20 }
)

$CENARIOS = @(
    @{ nome = "leve";  arquivo = "locustfile_leve.py"  },
    @{ nome = "medio"; arquivo = "locustfile_medio.py" },
    @{ nome = "alto";  arquivo = "locustfile_alto.py"  }
)

# Garante que a subpasta existe
New-Item -ItemType Directory -Force -Path "./resultados/$ARQUITETURA" | Out-Null

Write-Host "======================================================"
Write-Host "  ARQUITETURA: $ARQUITETURA"
Write-Host "  INICIANDO BATERIA DE TESTES"
Write-Host "======================================================"

foreach ($cenario in $CENARIOS) {
    foreach ($carga in $CARGAS) {
        $nomeArquivo = "resultado_$($cenario.nome)_$($carga.nome)"

        Write-Host ""
        Write-Host "------------------------------------------------------"
        Write-Host "  CENARIO: $($cenario.nome.ToUpper()) | CARGA: $($carga.nome.ToUpper())"
        Write-Host "  Usuarios: $($carga.users) | Spawn rate: $($carga.rate)/s"
        Write-Host "  Duracao: $TEMPO_TESTE | ARQ: $ARQUITETURA"
        Write-Host "  CSV: $nomeArquivo"
        Write-Host "------------------------------------------------------"

        docker compose run --rm `
            -e LOCUST_FILE=$($cenario.arquivo) `
            -e ATTACKED_HOST=http://nginx `
            -e LOCUST_OPTS="--users $($carga.users) --spawn-rate $($carga.rate) --run-time $TEMPO_TESTE --headless --csv /locust/resultados/$ARQUITETURA/$nomeArquivo" `
            locust

        Write-Host "  Aguardando 60s antes do proximo teste..."
        Start-Sleep -Seconds 60
    }
}

Write-Host ""
Write-Host "======================================================"
Write-Host "  BATERIA $ARQUITETURA CONCLUIDA"
Write-Host "  CSVs salvos em ./resultados/$ARQUITETURA/"
Write-Host "======================================================"