#!/bin/bash

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 기본 경로 설정
DEFAULT_ROOT_PATH="$(pwd)/mongodb_02"
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
    echo "  -p path    Set custom root path for MongoDB installation (default: $DEFAULT_ROOT_PATH)"
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
    mkdir -p "$ROOT_PATH"/{config,data,backup,init,keyfile}
}

# 환경 변수 파일 생성
create_env_file() {
    log_info "Creating .env file..."
    cat > "$ROOT_PATH/.env" << EOL
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=admin_password
MONGO_INITDB_DATABASE=myapp
MONGO_PORT=27017
MONGO_EXPRESS_PORT=8081
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000

# Application Database
APP_DB_USERNAME=myapp
APP_DB_PASSWORD=myapp_password
EOL
}

# MongoDB 설정 파일 생성
create_mongo_config() {
    log_info "Creating MongoDB configuration..."
    cat > "$ROOT_PATH/config/mongod.conf" << EOL
# mongod.conf

storage:
  dbPath: /data/db
  journal:
    enabled: true
  wiredTiger:
    engineConfig:
      cacheSizeGB: 1

systemLog:
  destination: file
  path: /var/log/mongodb/mongod.log
  logAppend: true

net:
  port: 27017
  bindIp: 0.0.0.0

security:
  authorization: enabled
  keyFile: /keyfile/mongo-keyfile

replication:
  replSetName: rs0

operationProfiling:
  mode: slowOp
  slowOpThresholdMs: 100

setParameter:
  enableLocalhostAuthBypass: false
EOL
}

# 초기화 스크립트 생성
create_init_script() {
    log_info "Creating initialization script..."
    cat > "$ROOT_PATH/init/init-mongo.js" << EOL
// Application Database 및 유저 생성
db = db.getSiblingDB('myapp');

db.createUser({
    user: process.env.APP_DB_USERNAME,
    pwd: process.env.APP_DB_PASSWORD,
    roles: [
        { role: "readWrite", db: "myapp" }
    ]
});

// 샘플 컬렉션 생성
db.createCollection("users");
db.users.createIndex({ "email": 1 }, { unique: true });

// 읽기 전용 유저 생성
db.createUser({
    user: "readonly",
    pwd: "readonly_password",
    roles: [
        { role: "read", db: "myapp" }
    ]
});
EOL
}

# Docker Compose 파일 생성
create_docker_compose() {
    log_info "Creating docker-compose.yml..."
    cat > "$ROOT_PATH/docker-compose.yml" << EOL
services:
  mongodb:
    image: mongo:6.0
    container_name: mongodb
    environment:
      MONGO_INITDB_ROOT_USERNAME: \${MONGO_INITDB_ROOT_USERNAME}
      MONGO_INITDB_ROOT_PASSWORD: \${MONGO_INITDB_ROOT_PASSWORD}
      MONGO_INITDB_DATABASE: \${MONGO_INITDB_DATABASE}
      APP_DB_USERNAME: \${APP_DB_USERNAME}
      APP_DB_PASSWORD: \${APP_DB_PASSWORD}
    volumes:
      - ./data:/data/db
      - ./config:/etc/mongo
      - ./init:/docker-entrypoint-initdb.d
      - ./keyfile:/keyfile
    ports:
      - "\${MONGO_PORT}:27017"
    command: ["mongod", "--config", "/etc/mongo/mongod.conf"]
    healthcheck:
      test: [
        "CMD-SHELL",
        "mongosh \"mongodb://localhost:27017/\${MONGO_INITDB_DATABASE}\" --username \${MONGO_INITDB_ROOT_USERNAME} --password \${MONGO_INITDB_ROOT_PASSWORD} --authenticationDatabase admin --eval 'db.adminCommand(\"ping\")' --quiet || exit 1"
      ]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - mongo_network

  mongo-express:
    image: mongo-express
    container_name: mongo_express
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: \${MONGO_INITDB_ROOT_USERNAME}
      ME_CONFIG_MONGODB_ADMINPASSWORD: \${MONGO_INITDB_ROOT_PASSWORD}
      ME_CONFIG_MONGODB_URL: mongodb://\${MONGO_INITDB_ROOT_USERNAME}:\${MONGO_INITDB_ROOT_PASSWORD}@mongodb:27017/
      ME_CONFIG_BASICAUTH_USERNAME: admin
      ME_CONFIG_BASICAUTH_PASSWORD: admin_password
    ports:
      - "\${MONGO_EXPRESS_PORT}:8081"
    depends_on:
      - mongodb
    networks:
      - mongo_network

  prometheus:
    image: prom/prometheus
    container_name: prometheus
    ports:
      - "\${PROMETHEUS_PORT}:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - mongo_network

  mongodb-exporter:
    image: percona/mongodb_exporter:0.20
    container_name: mongodb_exporter
    command:
      - '--mongodb.uri=mongodb://\${MONGO_INITDB_ROOT_USERNAME}:\${MONGO_INITDB_ROOT_PASSWORD}@mongodb:27017'
    ports:
      - "9216:9216"
    depends_on:
      - mongodb
    networks:
      - mongo_network

  grafana:
    image: grafana/grafana
    container_name: grafana
    ports:
      - "\${GRAFANA_PORT}:3000"
    depends_on:
      - prometheus
    networks:
      - mongo_network

networks:
  mongo_network:
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
  - job_name: 'mongodb'
    static_configs:
      - targets: ['mongodb-exporter:9216']
EOL
}

# MongoDB Keyfile 생성
create_keyfile() {
    log_info "Creating MongoDB keyfile..."
    openssl rand -base64 756 > "$ROOT_PATH/keyfile/mongo-keyfile"
    chmod 400 "$ROOT_PATH/keyfile/mongo-keyfile"
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
EOL

    chmod +x "$ROOT_PATH/backup/backup.sh"
}

# 메인 실행 함수
main() {
    log_info "Starting MongoDB Docker setup in: $ROOT_PATH"
    
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
    create_mongo_config
    create_init_script
    create_docker_compose
    create_prometheus_config
    create_keyfile
    create_backup_script

    log_info "Setup completed successfully!"
    log_info "To start the services, run:"
    echo -e "${GREEN}cd $ROOT_PATH && docker compose up -d${NC}"
}

# 스크립트 실행
main