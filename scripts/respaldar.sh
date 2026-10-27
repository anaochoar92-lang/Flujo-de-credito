#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/.."
mkdir -p backups
name="mba_$(date +%Y%m%d_%H%M%S).dump"
docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc -f /tmp/mba_respaldo.dump'
cid=$(docker compose ps -q db)
[ -n "$cid" ] || { echo 'PostgreSQL no está iniciado' >&2; exit 1; }
docker cp "$cid:/tmp/mba_respaldo.dump" "backups/$name" >/dev/null
docker compose exec -T db rm -f /tmp/mba_respaldo.dump
echo "Respaldo: backups/$name"
