#!/bin/bash

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 기본 경로 설정
DEFAULT_ROOT_PATH="$(pwd)/redis_02"
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
    echo "  -p path    Set custom root path for Redis installation (default: $DEFAULT_ROOT_PATH)"
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
    mkdir -p "$ROOT_PATH"/{config,data,backup}
    mkdir -p "$ROOT_PATH/data"/{master,replica,sentinel}
}

# 환경 변수 파일 생성
create_env_file() {
    log_info "Creating .env file..."
    cat > "$ROOT_PATH/.env" << EOL
REDIS_PASSWORD=redis_password
REDIS_PORT=6379
REDIS_REPLICA_PORT=6380
SENTINEL_PORT=26379
REDIS_COMMANDER_PORT=8081
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
EOL
}

# Redis 마스터 설정 파일 생성
create_redis_master_config() {
    log_info "Creating Redis master configuration..."
    cat > "$ROOT_PATH/config/redis-master.conf" << EOL
# 기본 설정
port 6379
bind 0.0.0.0
daemonize no
supervised systemd
dir /data

# 보안 설정
requirepass \${REDIS_PASSWORD}
masterauth \${REDIS_PASSWORD}

# 퍼시스턴스 설정
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# 스냅샷 설정
save 900 1
save 300 10
save 60 10000

# 메모리 설정
maxmemory 1gb
maxmemory-policy allkeys-lru
maxmemory-samples 5

# 느린 로그 설정
slowlog-log-slower-than 10000
slowlog-max-len 128

# 보안 설정
rename-command FLUSHALL ""
rename-command FLUSHDB ""
rename-command DEBUG ""
EOL
}

# Redis 레플리카 설정 파일 생성
create_redis_replica_config() {
    log_info "Creating Redis replica configuration..."
    cat > "$ROOT_PATH/config/redis-replica.conf" << EOL
# 기본 설정
port 6380
bind 0.0.0.0
daemonize no
supervised systemd
dir /data

# 복제 설정
replicaof redis-master 6379
masterauth \${REDIS_PASSWORD}

# 보안 설정
requirepass \${REDIS_PASSWORD}

# 퍼시스턴스 설정
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec

# 메모리 설정
maxmemory 1gb
maxmemory-policy allkeys-lru
maxmemory-samples 5
EOL
}

# Sentinel 설정 파일 생성
create_sentinel_config() {
    log_info "Creating Sentinel configuration..."
    cat > "$ROOT_PATH/config/sentinel.conf" << EOL
port 26379
dir /data
sentinel deny-scripts-reconfig yes

sentinel monitor mymaster redis-master 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 60000
sentinel auth-pass mymaster \${REDIS_PASSWORD}
EOL
}

# Docker Compose 파일 생성
create_docker_compose() {
    log_info "Creating docker-compose.yml..."
    cat > "$ROOT_PATH/docker-compose.yml" << EOL
services:
  redis-master:
    image: redis:7.0
    container_name: redis_master
    command: redis-server /usr/local/etc/redis/redis.conf
    environment:
      - REDIS_PASSWORD=\${REDIS_PASSWORD}
    volumes:
      - ./config/redis-master.conf:/usr/local/etc/redis/redis.conf
      - ./data/master:/data
    ports:
      - "\${REDIS_PORT}:6379"
    networks:
      - redis_network
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "\${REDIS_PASSWORD}", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis-replica:
    image: redis:7.0
    container_name: redis_replica
    command: redis-server /usr/local/etc/redis/redis.conf
    environment:
      - REDIS_PASSWORD=\${REDIS_PASSWORD}
    volumes:
      - ./config/redis-replica.conf:/usr/local/etc/redis/redis.conf
      - ./data/replica:/data
    ports:
      - "\${REDIS_REPLICA_PORT}:6380"
    depends_on:
      - redis-master
    networks:
      - redis_network
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "\${REDIS_PASSWORD}", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis-sentinel:
    image: redis:7.0
    container_name: redis_sentinel
    command: redis-sentinel /usr/local/etc/redis/sentinel.conf
    environment:
      - REDIS_PASSWORD=\${REDIS_PASSWORD}
    volumes:
      - ./config/sentinel.conf:/usr/local/etc/redis/sentinel.conf
      - ./data/sentinel:/data
    ports:
      - "\${SENTINEL_PORT}:26379"
    depends_on:
      - redis-master
      - redis-replica
    networks:
      - redis_network

  redis-commander:
    image: rediscommander/redis-commander:latest
    container_name: redis_commander
    environment:
      - REDIS_HOSTS=master:redis-master:6379:0:\${REDIS_PASSWORD},replica:redis-replica:6380:0:\${REDIS_PASSWORD}
    ports:
      - "\${REDIS_COMMANDER_PORT}:8081"
    depends_on:
      - redis-master
      - redis-replica
    networks:
      - redis_network

  redis-exporter:
    image: oliver006/redis_exporter
    container_name: redis_exporter
    command: --redis.password=\${REDIS_PASSWORD} --redis.addr=redis-master:6379
    ports:
      - "9121:9121"
    networks:
      - redis_network

  prometheus:
    image: prom/prometheus
    container_name: prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "\${PROMETHEUS_PORT}:9090"
    networks:
      - redis_network

  grafana:
    image: grafana/grafana
    container_name: grafana
    ports:
      - "\${GRAFANA_PORT}:3000"
    depends_on:
      - prometheus
    networks:
      - redis_network

networks:
  redis_network:
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
  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
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
REDIS_PASSWORD="${REDIS_PASSWORD:-redis_password}"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

mkdir -p "$BACKUP_DIR"

docker exec -e REDISCLI_AUTH="$REDIS_PASSWORD" redis_master redis-cli SAVE

docker cp redis_master:/data "$TMP_DIR/redis-data"
tar -C "$TMP_DIR" -czf "$BACKUP_DIR/redis_backup_$TIMESTAMP.tar.gz" redis-data

find "$BACKUP_DIR" -name "redis_backup_*.tar.gz" -mtime +30 -delete
EOL

    chmod +x "$ROOT_PATH/backup/backup.sh"
}

# 메인 실행 함수
main() {
    log_info "Starting Redis Docker setup in: $ROOT_PATH"
    
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
    create_redis_master_config
    create_redis_replica_config
    create_sentinel_config
    create_docker_compose
    create_prometheus_config
    create_backup_script

    log_info "Setup completed successfully!"
    log_info "To start the services, run:"
    echo -e "${GREEN}cd $ROOT_PATH && docker compose up -d${NC}"
}

# 스크립트 실행
main