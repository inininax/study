#!/usr/bin/env bash
#
# setup_mongodb.sh
# - Docker + MongoDB 단독 환경을 위한 기본 디렉터리/파일 생성 스크립트
# - 실행하면 my-mongodb-setup/ 디렉터리를 생성하고, 필요한 설정 파일들을 생성합니다.

set -e

PROJECT_DIR="mongodb_01"

echo "======================================================"
echo "  Docker + MongoDB Setup Script"
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

MONGO_INITDB_ROOT_USERNAME=rootuser
MONGO_INITDB_ROOT_PASSWORD=rootpw
MONGO_INITDB_DATABASE=mydb

# 호스트에서 사용할 포트
MONGO_PORT=27017
EOF

# 3) config 디렉터리 및 mongod.conf 생성
echo "[3/5] config 디렉터리 생성 및 mongod.conf 생성"
mkdir -p "${PROJECT_DIR}/config"

cat << 'EOF' > "${PROJECT_DIR}/config/mongod.conf"
# mongod.conf (MongoDB Custom Configuration)
# 실무 환경에 맞춰 세부 튜닝 가능.

# net:
  port: 27017
  bindIp: 0.0.0.0   # 컨테이너 내부뿐만 아니라 외부 접근도 가능하도록 설정

# storage:
  dbPath: /data/db
  journal:
    enabled: true

# systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log

# processManagement:
  fork: false

# security:
  # authorization: enabled   # 인증을 사용하려면 아래와 같이 설정
EOF

# 4) docker-compose.yml 생성
echo "[4/5] docker-compose.yml 파일 생성"
cat << 'EOF' > "${PROJECT_DIR}/docker-compose.yml"
services:
  mongodb:
    image: mongo:6.0
    container_name: my-mongodb
    restart: always
    ports:
      - "${MONGO_PORT}:27017"
    env_file:
      - .env
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_INITDB_ROOT_USERNAME}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_INITDB_ROOT_PASSWORD}
      MONGO_INITDB_DATABASE: ${MONGO_INITDB_DATABASE}

    command: ["--config", "/etc/mongod.conf"]

    volumes:
      # (1) 데이터 영속화 볼륨 (MongoDB 기본 데이터 경로: /data/db)
      - db-data:/data/db

      # (2) 커스텀 설정 파일 마운트
      - ./config/mongod.conf:/etc/mongod.conf

    healthcheck:
      test: [
        "CMD-SHELL",
        "mongosh \"mongodb://localhost:27017/${MONGO_INITDB_DATABASE}\" --username ${MONGO_INITDB_ROOT_USERNAME} --password ${MONGO_INITDB_ROOT_PASSWORD} --authenticationDatabase admin --eval 'db.adminCommand(\"ping\")' --quiet || exit 1"
      ]
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
echo " 다음 명령어로 MongoDB 컨테이너를 실행할 수 있습니다:"
echo ""
echo "   cd ${PROJECT_DIR}"
echo "   docker compose up -d"
echo ""
echo " .env 파일에서 MongoDB 루트 유저, 루트 비밀번호, 초기 DB명, 포트 등을 변경할 수 있습니다."
echo "------------------------------------------------------"