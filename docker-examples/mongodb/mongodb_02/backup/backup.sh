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
DB_NAME="${MONGO_INITDB_DATABASE:-myapp}"
DB_USER="${MONGO_INITDB_ROOT_USERNAME:-admin}"
DB_PASSWORD="${MONGO_INITDB_ROOT_PASSWORD:-admin_password}"

mkdir -p "$BACKUP_DIR"

docker exec mongodb mongodump \
    --host localhost \
    --port 27017 \
    --username "$DB_USER" \
    --password "$DB_PASSWORD" \
    --authenticationDatabase admin \
    --db "$DB_NAME" \
    --archive | gzip > "$BACKUP_DIR/backup_$TIMESTAMP.gz"

find "$BACKUP_DIR" -name "backup_*.gz" -mtime +30 -delete
