# ----------------------------------------------------------------
#  Script PowerShell — Roda todos os testes e gera CSVs
#  Execute: .\rodar_testes.ps1
# ----------------------------------------------------------------

$TEMPO_TESTE = "60s"

# Configuracoes de carga
$CARGAS = @(
    @{ nome = "baixa"; users = 100;   rate = 10  },
    @{ nome = "media"; users = 200;  rate = 50  },
    @{ nome = "alta";  users = 350; rate = 100 }
)

# Cenarios de teste e seus locustfiles
$CENARIOS = @(
    @{ nome = "leve";  arquivo = "locustfile_leve.py"  },
    @{ nome = "medio"; arquivo = "locustfile_medio.py" },
    @{ nome = "alto";  arquivo = "locustfile_alto.py"  }
)

Write-Host "======================================================"
Write-Host "  INICIANDO BATERIA DE TESTES"
Write-Host "======================================================"

foreach ($cenario in $CENARIOS) {
    foreach ($carga in $CARGAS) {
        $nomeArquivo = "resultado_$($cenario.nome)_$($carga.nome)"

        Write-Host ""
        Write-Host "------------------------------------------------------"
        Write-Host "  CENARIO: $($cenario.nome.ToUpper()) | CARGA: $($carga.nome.ToUpper())"
        Write-Host "  Usuarios: $($carga.users) | Spawn rate: $($carga.rate)/s"
        Write-Host "  Duracao: $TEMPO_TESTE"
        Write-Host "  CSV: $nomeArquivo"
        Write-Host "------------------------------------------------------"

        docker compose run --rm `
            -e LOCUST_FILE=$($cenario.arquivo) `
            -e ATTACKED_HOST=http://nginx `
            -e LOCUST_OPTS="--users $($carga.users) --spawn-rate $($carga.rate) --run-time $TEMPO_TESTE --headless --csv /locust/resultados/$nomeArquivo" `
            locust

        Write-Host "  Aguardando 30s antes do proximo teste..."
        Start-Sleep -Seconds 30
    }
}

Write-Host ""
Write-Host "======================================================"
Write-Host "  TODOS OS TESTES CONCLUIDOS"
Write-Host "  CSVs salvos em ./resultados/"
Write-Host "======================================================"