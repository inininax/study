#!/bin/bash

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 기본 경로 설정
DEFAULT_ROOT_PATH="$(pwd)/postgres_02"
ROOT_PATH=""

# 로그 함수
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 사용법 출력
print_usage() {
    echo "Usage: $0 [-p path]"
    echo "Options:"
    echo "  -p path    Set custom root path for postgres installation (default: $DEFAULT_ROOT_PATH)"
    echo "  -h         Show this help message"
}

# 명령행 인자 처리
while getopts "p:h" opt; do
    case $opt in
        p)
            ROOT_PATH="$OPTARG"
            ;;
        h)
            print_usage
            exit 0
            ;;
        \?)
            log_error "Invalid option: -$OPTARG"
            print_usage
            exit 1
            ;;
    esac
done

# ROOT_PATH가 지정되지 않았다면 기본값 사용
if [ -z "$ROOT_PATH" ]; then
    ROOT_PATH="$DEFAULT_ROOT_PATH"
fi

# 필수 디렉토리 생성
create_directories() {
    log_info "Creating necessary directories in $ROOT_PATH..."
    mkdir -p "$ROOT_PATH"/{init,conf,backup}
}

# 환경 변수 파일 생성
create_env_file() {
    log_info "Creating .env file..."
    cat > "$ROOT_PATH/.env" << EOL
POSTGRES_USER=myapp
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=myappdb
POSTGRES_PORT=5432
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
EOL
}

# PostgreSQL 설정 파일 생성
create_postgres_conf() {
    log_info "Creating PostgreSQL configuration..."
    cat > "$ROOT_PATH/conf/postgresql.conf" << EOL
shared_preload_libraries = 'pg_stat_statements'
shared_buffers = '1GB'
work_mem = '64MB'
maintenance_work_mem = '256MB'
effective_cache_size = '3GB'
synchronous_commit = off
max_connections = 100
random_page_cost = 1.1
effective_io_concurrency = 200
wal_level = logical
max_wal_size = '1GB'
pg_stat_statements.max = 10000
pg_stat_statements.track = all
EOL
}

# 초기화 SQL 스크립트 생성
create_init_sql() {
    log_info "Creating initialization SQL script..."
    cat > "$ROOT_PATH/init/01-init.sql" << EOL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- 읽기 전용 유저 생성
CREATE USER readonly WITH PASSWORD 'readonly_password';
GRANT CONNECT ON DATABASE myappdb TO readonly;
GRANT USAGE ON SCHEMA public TO readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly;
EOL
}

# Docker Compose 파일 생성
create_docker_compose() {
    log_info "Creating docker-compose.yml..."
    cat > "$ROOT_PATH/docker-compose.yml" << EOL
services:
  postgres:
    image: postgres:15.4
    container_name: postgres_db
    environment:
      POSTGRES_USER: \${POSTGRES_USER}
      POSTGRES_PASSWORD: \${POSTGRES_PASSWORD}
      POSTGRES_DB: \${POSTGRES_DB}
      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init:/docker-entrypoint-initdb.d
      - ./conf/postgresql.conf:/etc/postgresql/postgresql.conf
    ports:
      - "\${POSTGRES_PORT}:5432"
    command: postgres -c config_file=/etc/postgresql/postgresql.conf
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U \${POSTGRES_USER} -d \${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - postgres_network

  postgres-exporter:
    image: prometheuscommunity/postgres-exporter
    container_name: postgres_exporter
    environment:
      DATA_SOURCE_NAME: "postgresql://\${POSTGRES_USER}:\${POSTGRES_PASSWORD}@postgres:5432/\${POSTGRES_DB}?sslmode=disable"
    ports:
      - "9187:9187"
    depends_on:
      - postgres
    networks:
      - postgres_network

  prometheus:
    image: prom/prometheus
    container_name: prometheus
    ports:
      - "\${PROMETHEUS_PORT}:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - postgres_network

  grafana:
    image: grafana/grafana
    container_name: grafana
    ports:
      - "\${GRAFANA_PORT}:3000"
    depends_on:
      - prometheus
    networks:
      - postgres_network

networks:
  postgres_network:
    driver: bridge

volumes:
  postgres_data:
EOL
}

# Prometheus 설정 파일 생성
create_prometheus_config() {
    log_info "Creating Prometheus configuration..."
    cat > "$ROOT_PATH/prometheus.yml" << EOL
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']
EOL
}

# 백업 스크립트 생성
create_backup_script() {
    log_info "Creating backup script..."
    cat > "$ROOT_PATH/backup/backup.sh" << 'EOL'
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
EOL

    chmod +x "$ROOT_PATH/backup/backup.sh"
}

# 메인 실행 함수
main() {
    log_info "Starting PostgreSQL Docker setup in: $ROOT_PATH"
    
    # 기존 디렉토리 확인
    if [ -d "$ROOT_PATH" ] && [ "$(ls -A "$ROOT_PATH")" ]; then
        log_warn "$ROOT_PATH directory already exists and is not empty. Do you want to override? (y/n)"
        read -r answer
        if [ "$answer" != "y" ]; then
            log_error "Setup aborted."
            exit 1
        fi
        rm -rf "$ROOT_PATH"/*
    fi

    # 각 구성 요소 생성
    create_directories
    create_env_file
    create_postgres_conf
    create_init_sql
    create_docker_compose
    create_prometheus_config
    create_backup_script

    log_info "Setup completed successfully!"
    log_info "To start the services, run:"
    echo -e "${GREEN}cd $ROOT_PATH && docker compose up -d${NC}"
}

# 스크립트 실행
main