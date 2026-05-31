#!/usr/bin/env bash
#
# setup_postgres.sh
# - Docker + PostgreSQL 단독 환경을 위한 기본 디렉터리/파일 생성 스크립트
# - 실행하면 my-postgres-setup/ 디렉터리를 생성하고, 필요한 설정 파일들을 생성합니다.

set -e

PROJECT_DIR="postgres_01"

echo "======================================================"
echo "  Docker + PostgreSQL Setup Script"
echo "======================================================"
echo ""
echo "[1/5] 프로젝트 디렉터리 생성: ${PROJECT_DIR}"
echo ""

# 1) 디렉터리 생성
if [ -d "${PROJECT_DIR}" ]; then
  echo "이미 '${PROJECT_DIR}' 디렉터리가 존재합니다. 내용을 덮어쓰려면 계속 진행하세요."
  # 필요 시, 사용자 입력으로 계속 진행 여부 확인 로직 추가 가능
else
  mkdir -p "${PROJECT_DIR}"
fi

# 2) .env 파일 생성
echo "[2/5] .env 파일 생성"
cat << 'EOF' > "${PROJECT_DIR}/.env"
# 환경 변수 설정
# 실제 운영 환경에서는 비밀번호를 안전하게 보관하세요 (ex. Git에 올리지 않기)

POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=mydb

# 호스트에서 사용할 포트
DB_PORT=5432
EOF

# 3) config 디렉터리 및 PostgreSQL 설정 파일 생성
echo "[3/5] config 디렉터리 생성 및 설정 파일 생성"
mkdir -p "${PROJECT_DIR}/config"

# postgresql.conf
cat << 'EOF' > "${PROJECT_DIR}/config/postgresql.conf"
# PostgreSQL Custom Configuration
# (실무 환경에 맞게 세부 튜닝하세요)

listen_addresses = '*'
port = 5432

# 메모리 관련 예시
shared_buffers = 256MB
work_mem = 4MB
maintenance_work_mem = 64MB
max_connections = 100

# WAL & Checkpoint
wal_level = replica
synchronous_commit = on
checkpoint_timeout = 5min

# 로깅
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d.log'
log_min_messages = warning
log_min_error_statement = error
EOF

# pg_hba.conf
cat << 'EOF' > "${PROJECT_DIR}/config/pg_hba.conf"
# 호스트 기반 접근 제어 설정 (pg_hba.conf)

# 로컬 접근 (컨테이너 내부)
local   all             all                                     trust

# 특정 IP 대역만 허용하려면 예: 172.18.0.0/16
# host   all             all             172.18.0.0/16           md5

# 모든 외부 IP에서 접근 허용 (보안 이슈 주의)
host    all             all             0.0.0.0/0               md5
EOF

# 4) docker-compose.yml 생성
echo "[4/5] docker-compose.yml 파일 생성"
cat << 'EOF' > "${PROJECT_DIR}/docker-compose.yml"
services:
  postgres:
    image: postgres:15.2
    container_name: my-postgres
    restart: always
    ports:
      - "${DB_PORT}:5432"
    env_file:
      - .env
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}

    volumes:
      # (1) 데이터 영속화 볼륨
      - db-data:/var/lib/postgresql/data

      # (2) 설정 파일 마운트
      - ./config/postgresql.conf:/etc/postgresql/postgresql.conf
      - ./config/pg_hba.conf:/etc/postgresql/pg_hba.conf

    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  db-data:
EOF

# 5) 스크립트 완료 안내
echo "[5/5] 파일 생성 완료!"
echo ""
echo "------------------------------------------------------"
echo " 디렉터리 구조 확인:"
tree "${PROJECT_DIR}" || ls -R "${PROJECT_DIR}"
echo "------------------------------------------------------"
echo " 다음 명령어로 PostgreSQL 컨테이너를 실행할 수 있습니다:"
echo ""
echo "   cd ${PROJECT_DIR}"
echo "   docker compose up -d"
echo ""
echo " .env 파일에서 DB 유저/패스워드/DB명 등을 변경하고, 포트도 조정할 수 있습니다."
echo "------------------------------------------------------"
