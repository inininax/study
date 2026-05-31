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
REDIS_PASSWORD="${REDIS_PASSWORD:-redis_password}"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

mkdir -p "$BACKUP_DIR"

docker exec -e REDISCLI_AUTH="$REDIS_PASSWORD" redis_master redis-cli SAVE

docker cp redis_master:/data "$TMP_DIR/redis-data"
tar -C "$TMP_DIR" -czf "$BACKUP_DIR/redis_backup_$TIMESTAMP.tar.gz" redis-data

find "$BACKUP_DIR" -name "redis_backup_*.tar.gz" -mtime +30 -delete
