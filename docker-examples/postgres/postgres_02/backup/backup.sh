#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$ROOT_DIR/.env"

if [ -f "$ENV_FILE" ]; then
    set -a
    . "$ENV_FILE"
    set +a
fi

BACKUP_DIR="${BACKUP_DIR:-$SCRIPT_DIR}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
DB_NAME="${POSTGRES_DB:-myappdb}"
DB_USER="${POSTGRES_USER:-myapp}"
DB_PASSWORD="${POSTGRES_PASSWORD:-secure_password}"

mkdir -p "$BACKUP_DIR"

docker exec -e PGPASSWORD="$DB_PASSWORD" postgres_db \
    pg_dump -U "$DB_USER" "$DB_NAME" \
    | gzip > "$BACKUP_DIR/backup_$TIMESTAMP.sql.gz"

find "$BACKUP_DIR" -name "backup_*.sql.gz" -mtime +30 -delete
