# Windows PowerShell 5.1+/PowerShell 7. Abrir PowerShell en raíz del repositorio.
$ErrorActionPreference = 'Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))
docker compose version | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'Instala Docker Desktop y habilita Docker Compose v2.' }
if (!(Test-Path '.env')) {
  $template = Get-Content '.env.docker.example' -Raw
  $buf = New-Object byte[] 24
  $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
  try { $rng.GetBytes($buf) } finally { $rng.Dispose() }
  $secret = [System.BitConverter]::ToString($buf).Replace('-', '').ToLowerInvariant()
  $template = $template.Replace('REEMPLAZAR_POR_UN_SECRETO_ALEATORIO', $secret)
  [System.IO.File]::WriteAllText((Join-Path (Get-Location) '.env'), $template, (New-Object System.Text.UTF8Encoding($false)))
  Write-Host 'Generado .env privado con contraseña aleatoria.'
}
New-Item -ItemType Directory -Force -Path 'exports','backups' | Out-Null
docker compose up -d --build --wait
if ($LASTEXITCODE -ne 0) { throw 'Falló Docker Compose; ejecuta docker compose ps y docker compose logs api.' }
Write-Host 'MVP disponible en http://127.0.0.1:8088'
Write-Host 'API: http://127.0.0.1:8088/docs'
Write-Host 'ETL: docker compose run --rm etl'
