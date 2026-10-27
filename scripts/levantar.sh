#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/.."
docker compose version >/dev/null
if [ ! -f .env ]; then
  if [ ! -r /dev/urandom ]; then echo 'No se puede generar contraseña aleatoria' >&2; exit 1; fi
  PASSWORD=$(od -An -N24 -tx1 /dev/urandom | tr -d ' \n')
  sed "s/REEMPLAZAR_POR_UN_SECRETO_ALEATORIO/$PASSWORD/" .env.docker.example > .env
  chmod 600 .env
  echo 'Generado .env privado.'
fi
mkdir -p exports backups
docker compose up -d --build --wait
echo 'MVP: http://127.0.0.1:8088 (puerto configurable MVP_PORT en .env)'
echo 'ETL: docker compose run --rm etl'
