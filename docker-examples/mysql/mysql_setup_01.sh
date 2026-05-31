#!/usr/bin/env bash
#
# setup_mysql.sh
# - Docker + MySQL 단독 환경을 위한 기본 디렉터리/파일 생성 스크립트
# - 실행하면 my-mysql-setup/ 디렉터리를 생성하고, 필요한 설정 파일들을 생성합니다.

set -e

PROJECT_DIR="mysql_01"

echo "======================================================"
echo "  Docker + MySQL Setup Script"
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

MYSQL_ROOT_PASSWORD=rootpw
MYSQL_DATABASE=mydb
MYSQL_USER=myuser
MYSQL_PASSWORD=mypassword

# 호스트에서 사용할 포트
DB_PORT=3306
EOF

# 3) config 디렉터리 및 MySQL 설정 파일(my.cnf) 생성
echo "[3/5] config 디렉터리 생성 및 my.cnf 생성"
mkdir -p "${PROJECT_DIR}/config"

cat << 'EOF' > "${PROJECT_DIR}/config/my.cnf"
# my.cnf (MySQL Custom Configuration)
# 실무 환경에 맞게 세부 튜닝 가능.
# 공식 Docker 이미지에서 /etc/mysql/conf.d/*.cnf 를 자동 로드합니다.

[mysqld]
# 네트워크
bind-address            = 0.0.0.0
port                    = 3306

# 기본 문자셋/Collation
character-set-server    = utf8mb4
collation-server        = utf8mb4_unicode_ci

# 최대 연결 수
max_connections         = 200

# 로그 설정 예시
slow_query_log          = 1
slow_query_log_file     = /var/log/mysql/slow.log
long_query_time         = 1

# 기타 튜닝 파라미터 (예시)
innodb_buffer_pool_size = 256M
innodb_log_file_size    = 64M
EOF

# 4) docker-compose.yml 생성
echo "[4/5] docker-compose.yml 파일 생성"
cat << 'EOF' > "${PROJECT_DIR}/docker-compose.yml"
services:
  mysql:
    image: mysql:8.0
    container_name: my-mysql
    restart: always
    ports:
      - "${DB_PORT}:3306"
    env_file:
      - .env
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}

    volumes:
      # (1) 데이터 영속화 볼륨
      - db-data:/var/lib/mysql

      # (2) 커스텀 설정 파일 마운트
      #     /etc/mysql/conf.d/*.cnf는 Docker 공식 MySQL 이미지에서 자동 로드
      - ./config/my.cnf:/etc/mysql/conf.d/my.cnf

    healthcheck:
      test: ["CMD-SHELL", "mysqladmin ping -h localhost -p${MYSQL_ROOT_PASSWORD} --silent || exit 1"]
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
echo " 다음 명령어로 MySQL 컨테이너를 실행할 수 있습니다:"
echo ""
echo "   cd ${PROJECT_DIR}"
echo "   docker compose up -d"
echo ""
echo " .env 파일에서 MySQL 루트 패스워드, DB 이름, 유저, 포트 등을 변경할 수 있습니다."
echo "------------------------------------------------------"