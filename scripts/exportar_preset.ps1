$ErrorActionPreference = 'Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))
docker compose run --rm etl
if ($LASTEXITCODE -ne 0) { throw 'ETL fallida; verifica docker compose logs db' }
Write-Host 'CSV y manifiesto disponibles en .\exports\'
