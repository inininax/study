#!/usr/bin/env bash
#
# setup_redis.sh
# - Docker + Redis 단독 환경을 위한 기본 디렉터리/파일 생성 스크립트
# - 실행하면 my-redis-setup/ 디렉터리를 생성하고, 필요한 설정 파일들을 생성합니다.

set -e

PROJECT_DIR="redis_01"

echo "======================================================"
echo "  Docker + Redis Setup Script"
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

REDIS_PASSWORD=myredispass

# 호스트에서 사용할 포트
REDIS_PORT=6379
EOF

# 3) config 디렉터리 및 redis.conf 생성
echo "[3/5] config 디렉터리 생성 및 redis.conf 생성"
mkdir -p "${PROJECT_DIR}/config"

cat << 'EOF' > "${PROJECT_DIR}/config/redis.conf"
#################################
# redis.conf (커스텀 설정 예시)
#################################

# 포트 설정 (Docker 컨테이너 내부 포트: 6379)
port 6379

# 바인드: 0.0.0.0으로 모든 인터페이스에서 접근 가능
bind 0.0.0.0

# 보안: Redis AUTH 사용 (이 스크립트에서는 Docker Compose에서 --requirepass로 전달)
# requirepass MY_REDIS_PASSWORD    # <- 아래 command 옵션에서 환경변수로 대체

# Append-only 파일 설정 (데이터 영속성 강화)
appendonly yes
appendfilename "appendonly.aof"

# RDB 스냅샷 (기본값 예시)
save 900 1     # 15분(900초) 동안 변경이 1개 이상이면 덤프
save 300 10    # 5분(300초) 동안 변경이 10개 이상이면 덤프
save 60 10000  # 1분(60초) 동안 변경이 10000개 이상이면 덤프

# 로그 설정
logfile "/var/log/redis/redis-server.log"
loglevel notice
EOF

# 4) docker-compose.yml 생성
echo "[4/5] docker-compose.yml 파일 생성"
cat << 'EOF' > "${PROJECT_DIR}/docker-compose.yml"
services:
  redis:
    image: redis:7.0
    container_name: my-redis
    restart: always
    ports:
      - "${REDIS_PORT}:6379"
    env_file:
      - .env

    command: >
      sh -c "redis-server /usr/local/etc/redis/redis.conf
      --requirepass \$REDIS_PASSWORD"

    volumes:
      # (1) 데이터 영속화 볼륨
      - redis-data:/data

      # (2) 커스텀 설정 파일 마운트
      # 공식 redis 이미지에서는 /usr/local/etc/redis/ 이하 설정 파일을 자동 로드
      - ./config/redis.conf:/usr/local/etc/redis/redis.conf

    healthcheck:
      test: ["CMD", "redis-cli", "-a", "${REDIS_PASSWORD}", "PING"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  redis-data:
EOF

# 5) 스크립트 완료 안내
echo "[5/5] 파일 생성 완료!"
echo ""
echo "------------------------------------------------------"
echo " 디렉터리 구조 확인:"
tree "${PROJECT_DIR}" || ls -R "${PROJECT_DIR}"
echo "------------------------------------------------------"
echo " 다음 명령어로 Redis 컨테이너를 실행할 수 있습니다:"
echo ""
echo "   cd ${PROJECT_DIR}"
echo "   docker compose up -d"
echo ""
echo " .env 파일에서 Redis 비밀번호와 포트를 변경할 수 있습니다."
echo "------------------------------------------------------"