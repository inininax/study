# ELK Stack Example Makefile
# GitHub: https://github.com/kyungseok-lee/elk-examples

.PHONY: help build up down logs clean dev-server dev-client setup

# 기본 타겟
help:
	@echo "ELK Stack Example 프로젝트"
	@echo "GitHub: https://github.com/kyungseok-lee/elk-examples"
	@echo ""
	@echo "사용 가능한 명령어:"
	@echo "  make setup       - 프로젝트 초기 설정"
	@echo "  make up          - 모든 서비스 시작 (Docker Compose)"
	@echo "  make down        - 모든 서비스 중지"
	@echo "  make logs        - 서비스 로그 확인"
	@echo "  make build       - 모든 이미지 빌드"
	@echo "  make clean       - 컨테이너 및 볼륨 정리"
	@echo "  make dev-server  - Go 서버 로컬 개발 모드"
	@echo "  make dev-client  - Next.js 클라이언트 로컬 개발 모드"
	@echo "  make status      - 서비스 상태 확인"
	@echo "  make filebeat    - Filebeat 상태 확인"

# 프로젝트 초기 설정
setup:
	@echo "🔧 프로젝트 초기 설정을 시작합니다..."
	mkdir -p logs data/elasticsearch data/logstash data/filebeat/modules.d
	@echo "✅ 초기 설정이 완료되었습니다!"

# Docker Compose 명령어
up:
	@echo "🚀 ELK Stack 서비스들을 시작합니다..."
	docker compose up -d
	@echo "⏳ 서비스 준비 대기 중..."
	sleep 45
	@echo "✅ 서비스가 시작되었습니다!"
	@echo "🌐 Next.js 클라이언트: http://localhost:3000"
	@echo "🌐 Kibana 대시보드: http://localhost:5601"
	@echo "🌐 Elasticsearch: http://localhost:9200"

down:
	@echo "🛑 서비스들을 중지합니다..."
	docker compose down

logs:
	@echo "📋 서비스 로그를 확인합니다..."
	docker compose logs -f

build:
	@echo "🔨 모든 이미지를 빌드합니다..."
	docker compose build

clean:
	@echo "🧹 컨테이너와 볼륨을 정리합니다..."
	docker compose down -v
	docker system prune -f

status:
	@echo "🔍 서비스 상태를 확인합니다..."
	docker compose ps

# 로컬 개발 명령어
dev-server:
	@echo "🔧 Go 서버를 로컬 개발 모드로 실행합니다..."
	cd server && go run main.go

dev-client:
	@echo "🔧 Next.js 클라이언트를 로컬 개발 모드로 실행합니다..."
	cd client && npm run dev

# 의존성 설치
install-server:
	@echo "📦 Go 서버 의존성을 설치합니다..."
	cd server && go mod tidy

install-client:
	@echo "📦 Next.js 클라이언트 의존성을 설치합니다..."
	cd client && npm install

# 전체 설치
install: install-server install-client
	@echo "✅ 모든 의존성이 설치되었습니다!"

# 테스트
test-server:
	@echo "🧪 Go 서버 테스트를 실행합니다..."
	cd server && go test ./...

test-client:
	@echo "🧪 Next.js 클라이언트 테스트를 실행합니다..."
	cd client && npm test

# 전체 테스트
test: test-server test-client
	@echo "✅ 모든 테스트가 완료되었습니다!"

# Filebeat 상태 확인
filebeat:
	@echo "🔍 Filebeat 상태를 확인합니다..."
	docker compose logs filebeat
	@echo ""
	@echo "📊 Filebeat 통계:"
	docker compose exec filebeat filebeat test output

# 로그 파일 확인
check-logs:
	@echo "📋 로그 파일을 확인합니다..."
	@echo "=== Go 서버 로그 ==="
	@ls -la logs/ 2>/dev/null || echo "로그 파일이 없습니다."
	@echo ""
	@echo "=== Docker 컨테이너 로그 ==="
	docker compose logs --tail=10

# 데이터 백업
backup:
	@echo "💾 데이터를 백업합니다..."
	tar -czf backup-$(shell date +%Y%m%d-%H%M%S).tar.gz data/ logs/
	@echo "✅ 백업이 완료되었습니다: backup-$(shell date +%Y%m%d-%H%M%S).tar.gz"
