$ErrorActionPreference = 'Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))
if (!(Test-Path '.env')) { throw 'Primero ejecuta levantar.ps1' }
New-Item -ItemType Directory -Force -Path 'backups' | Out-Null
$filename = 'mba_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.dump'
# Evita redireccionar binarios desde PowerShell (podría modificar bytes).
$cmd = 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc -f /tmp/mba_respaldo.dump'
docker compose exec -T db sh -c $cmd
if ($LASTEXITCODE -ne 0) { throw 'pg_dump falló' }
$containerId = (docker compose ps -q db).Trim()
if (-not $containerId) { throw 'No se encontró el contenedor PostgreSQL' }
docker cp "${containerId}:/tmp/mba_respaldo.dump" "backups/$filename"
if ($LASTEXITCODE -ne 0) { throw 'docker cp falló' }
docker compose exec -T db rm -f /tmp/mba_respaldo.dump | Out-Null
Write-Host "Respaldo verificado: backups/$filename"
