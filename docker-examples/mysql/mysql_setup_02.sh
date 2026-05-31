#!/bin/bash

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 기본 경로 설정
DEFAULT_ROOT_PATH="$(pwd)/mysql_02"
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
    echo "  -p path    Set custom root path for MySQL installation (default: $DEFAULT_ROOT_PATH)"
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
    mkdir -p "$ROOT_PATH"/{init,conf,backup,data}
}

# 환경 변수 파일 생성
create_env_file() {
    log_info "Creating .env file..."
    cat > "$ROOT_PATH/.env" << EOL
MYSQL_ROOT_PASSWORD=root_password
MYSQL_DATABASE=myapp
MYSQL_USER=myapp
MYSQL_PASSWORD=myapp_password
MYSQL_PORT=3306
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
EOL
}

# MySQL 설정 파일 생성
create_mysql_conf() {
    log_info "Creating MySQL configuration..."
    cat > "$ROOT_PATH/conf/my.cnf" << EOL
[mysqld]
# 기본 설정
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
default_authentication_plugin = mysql_native_password

# 성능 최적화
innodb_buffer_pool_size = 1G
innodb_log_file_size = 256M
innodb_log_buffer_size = 64M
innodb_file_per_table = 1
innodb_flush_log_at_trx_commit = 2
innodb_flush_method = O_DIRECT

# 커넥션 설정
max_connections = 1000
thread_cache_size = 128
table_open_cache = 4000

# 쿼리 캐시 (MySQL 8.0에서는 제거됨)
# query_cache_size = 0
# query_cache_type = 0

# 슬로우 쿼리 설정
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow_query.log
long_query_time = 1

# 바이너리 로그 설정
server_id = 1
log_bin = mysql-bin
binlog_format = ROW
sync_binlog = 0
expire_logs_days = 7

[client]
default-character-set = utf8mb4

[mysql]
default-character-set = utf8mb4
EOL
}

# 초기화 SQL 스크립트 생성
create_init_sql() {
    log_info "Creating initialization SQL script..."
    cat > "$ROOT_PATH/init/01-init.sql" << EOL
-- 읽기 전용 유저 생성
CREATE USER 'readonly'@'%' IDENTIFIED BY 'readonly_password';
GRANT SELECT ON myapp.* TO 'readonly'@'%';

-- 타임존 설정
SET GLOBAL time_zone = '+09:00';
SET time_zone = '+09:00';

-- 샘플 테이블 생성
CREATE TABLE IF NOT EXISTS \`users\` (
  \`id\` bigint NOT NULL AUTO_INCREMENT,
  \`email\` varchar(255) NOT NULL,
  \`name\` varchar(255) NOT NULL,
  \`created_at\` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  \`updated_at\` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (\`id\`),
  UNIQUE KEY \`uk_users_email\` (\`email\`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
EOL
}

# Docker Compose 파일 생성
create_docker_compose() {
    log_info "Creating docker-compose.yml..."
    cat > "$ROOT_PATH/docker-compose.yml" << EOL
services:
  mysql:
    image: mysql:8.0
    container_name: mysql_db
    environment:
      MYSQL_ROOT_PASSWORD: \${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: \${MYSQL_DATABASE}
      MYSQL_USER: \${MYSQL_USER}
      MYSQL_PASSWORD: \${MYSQL_PASSWORD}
    volumes:
      - ./data:/var/lib/mysql
      - ./conf/my.cnf:/etc/mysql/conf.d/my.cnf
      - ./init:/docker-entrypoint-initdb.d
    ports:
      - "\${MYSQL_PORT}:3306"
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u\${MYSQL_USER}", "-p\${MYSQL_PASSWORD}"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - mysql_network

  prometheus:
    image: prom/prometheus
    container_name: prometheus
    ports:
      - "\${PROMETHEUS_PORT}:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - mysql_network

  grafana:
    image: grafana/grafana
    container_name: grafana
    ports:
      - "\${GRAFANA_PORT}:3000"
    depends_on:
      - prometheus
    networks:
      - mysql_network

  mysqld-exporter:
    image: prom/mysqld-exporter
    container_name: mysqld_exporter
    ports:
      - "9104:9104"
    environment:
      DATA_SOURCE_NAME: "\${MYSQL_USER}:\${MYSQL_PASSWORD}@(mysql:3306)/"
    depends_on:
      - mysql
    networks:
      - mysql_network

networks:
  mysql_network:
    driver: bridge
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
  - job_name: 'mysqld'
    static_configs:
      - targets: ['mysqld-exporter:9104']
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
DB_NAME="${MYSQL_DATABASE:-myapp}"
DB_USER="${MYSQL_USER:-myapp}"
DB_PASSWORD="${MYSQL_PASSWORD:-myapp_password}"

mkdir -p "$BACKUP_DIR"

# Use MYSQL_PWD so the password is not exposed as a mysqldump CLI argument.
docker exec -e MYSQL_PWD="$DB_PASSWORD" mysql_db \
    mysqldump -u"$DB_USER" "$DB_NAME" \
    | gzip > "$BACKUP_DIR/backup_$TIMESTAMP.sql.gz"

find "$BACKUP_DIR" -name "backup_*.sql.gz" -mtime +30 -delete
EOL

    chmod +x "$ROOT_PATH/backup/backup.sh"
}

# 메인 실행 함수
main() {
    log_info "Starting MySQL Docker setup in: $ROOT_PATH"
    
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
    create_mysql_conf
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