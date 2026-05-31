# Go Workspace Examples

이 프로젝트는 Go 1.18+의 **workspace** 기능을 활용한 실무 환경에서 사용 가능한 다양한 예제들을 제공합니다.

## 🚀 빠른 시작

### 1. 프로젝트 클론 및 설정
```bash
git clone https://github.com/kyungseok-lee/go-work-examples.git
cd go-work-examples

# 워크스페이스 동기화
go work sync

# 모든 모듈 의존성 정리
./scripts/sync-all.sh
```

### 2. 워크스페이스 데모 실행
```bash
# Go workspace의 모든 기능을 보여주는 종합 데모
cd examples/workspace-demo
go run main.go
```

### 3. 마이크로서비스 실행
```bash
# 터미널 1: User Service
cd services/user-service
go run main.go

# 터미널 2: Order Service  
cd services/order-service
go run main.go

# 터미널 3: Notification Service
cd services/notification-service
go run main.go
```

## 📁 프로젝트 구조

```
go-work-examples/
├── go.work                           # Go workspace 설정 파일
├── shared/                          # 공유 라이브러리
│   ├── types/                       # 공통 타입 정의
│   ├── utils/                       # 유틸리티 함수
│   ├── events/                      # 이벤트 시스템
│   ├── errors/                      # 공통 에러 타입
│   ├── config/                      # 설정 관리
│   ├── logger/                      # 구조화된 로깅
│   └── middleware/                  # 공통 미들웨어
├── services/                        # 마이크로서비스들
│   ├── user-service/               # 사용자 관리 서비스 (포트 8080)
│   ├── order-service/              # 주문 관리 서비스 (포트 8081)
│   └── notification-service/       # 알림 서비스 (포트 8082)
├── tools/                          # 개발 도구들
│   ├── cli/                        # CLI 도구
│   └── migration/                  # 데이터베이스 마이그레이션 도구
├── examples/                       # 사용 예제
│   ├── library-consumer/           # 공유 라이브러리 사용 예제
│   └── workspace-demo/             # Go workspace 기능 데모
└── scripts/                        # 편리한 스크립트들
    ├── sync-all.sh                 # 전체 동기화
    ├── update-all.sh               # 의존성 업데이트
    └── clean-all.sh                # 모듈 정리
```

> **핵심 특징**: Go workspace의 네이티브 기능을 사용하여 `replace` 디렉티브 없이 로컬 모듈을 직접 참조합니다.

## 🧪 테스트 및 사용법

### 1. 워크스페이스 데모 테스트
```bash
cd examples/workspace-demo
go run main.go
```

**예상 출력:**
```
=== Go Workspace Demo ===
This demo shows how Go workspaces enable seamless sharing of code across multiple modules

1. Configuration Management:
----------------------------
Server Address: localhost:8080
Database DSN: host=localhost port=5432 user=postgres password=password dbname=myapp sslmode=disable
Environment: development

2. Structured Logging:
---------------------
[2025-09-09 06:19:22] INFO workspace-demo: Application started map[env:development version:1.0.0]
[2025-09-09 06:19:22] WARN workspace-demo: This is a warning message

3. Shared Types and Validation:
-------------------------------
Created user: Workspace Demo User (demo@workspace.example)
✓ Email validation passed
✓ Name validation passed

4. Error Handling:
-----------------
Validation Error: validation error in field 'email': Invalid email format (HTTP Status: 400)
Not Found Error: User not found (ID: 123) (HTTP Status: 404)
Conflict Error: conflict in field 'email': Email already exists (HTTP Status: 409)

5. Event System:
---------------
Created event: user.created
Event ID: ebb5cbcd...
Event timestamp: 2025-09-09T06:19:22+09:00
[2025-09-09 06:19:22] INFO workspace-demo: Processing event map[event_id:ebb5cbcd... event_type:user.created]
[2025-09-09 06:19:23] INFO workspace-demo: Event processed successfully

6. Order Processing Example:
---------------------------
Created order: daab5bcb...
Total: $69.98
Items: 2
[2025-09-09 06:19:23] INFO workspace-demo: Processing event map[event_id:5fc1cea1... event_type:order.created]
[2025-09-09 06:19:23] INFO workspace-demo: Event processed successfully

7. Go Workspace Benefits Demonstrated:
--------------------------------------
✓ Shared configuration management across all modules
✓ Consistent logging format and levels
✓ Unified error handling with proper HTTP status codes
✓ Type-safe event system with shared data structures
✓ Common validation utilities
✓ No replace directives needed - direct local module references
✓ Single workspace for all related projects
✓ Consistent dependency versions across all modules
✓ Easy refactoring across the entire codebase

[2025-09-09 06:19:23] INFO workspace-demo: Demo completed successfully
=== Demo Complete ===
```

### 2. 마이크로서비스 테스트

#### 2.1 서비스 실행
```bash
# 터미널 1: User Service (포트 8080)
cd services/user-service
go run main.go

# 터미널 2: Order Service (포트 8081)
cd services/order-service
go run main.go

# 터미널 3: Notification Service (포트 8082)
cd services/notification-service
go run main.go
```

#### 2.2 API 테스트
```bash
# 1. 사용자 생성
curl -X POST http://localhost:8080/users \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test User"}'

# 2. 사용자 조회 (위에서 받은 ID 사용)
curl http://localhost:8080/users/{USER_ID}

# 3. 주문 생성
curl -X POST http://localhost:8081/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id":"USER_ID_HERE","items":[{"name":"Laptop","price":999.99,"quantity":1}]}'

# 4. 주문 상태 변경
curl -X PUT http://localhost:8081/orders/{ORDER_ID}/status \
  -H "Content-Type: application/json" \
  -d '{"status":"shipped"}'

# 5. 헬스체크
curl http://localhost:8080/health
curl http://localhost:8081/health
curl http://localhost:8082/health
```

### 3. CLI 도구 테스트
```bash
cd tools/cli

# 사용자 생성
go run main.go user create --email "user@example.com" --name "Test User"

# 사용자 조회
go run main.go user get {USER_ID}

# 주문 생성
go run main.go order create --user-id "{USER_ID}" --item-name "Laptop" --item-price 999.99 --item-quantity 1

# 주문 조회
go run main.go order get {ORDER_ID}

# 주문 상태 변경
go run main.go order update-status {ORDER_ID} shipped
```

### 4. 마이그레이션 도구 테스트
```bash
cd tools/migration

# 새 마이그레이션 생성
go run main.go create "add_user_profiles" --description "Add user profile tables"

# 마이그레이션 목록 보기
go run main.go list

# 마이그레이션 실행
go run main.go up

# 샘플 데이터 시딩
go run main.go seed
```

### 5. 라이브러리 사용 예제
```bash
cd examples/library-consumer
go run main.go
```

## 🔧 Go Workspace 관리

### 모듈 동기화
```bash
# 전체 워크스페이스 동기화
go work sync

# 모든 모듈 의존성 정리
./scripts/sync-all.sh

# 모든 의존성 업데이트
./scripts/update-all.sh

# 모든 모듈 정리 (캐시 포함)
./scripts/clean-all.sh
```

### 개별 모듈 관리
```bash
# 특정 모듈의 의존성 정리
cd services/user-service
go mod tidy

# 새 패키지 추가
go get github.com/redis/go-redis/v9

# 의존성 업데이트
go get -u ./...
```

## 📡 API 엔드포인트

### User Service (포트 8080)
- `POST /users` - 사용자 생성
- `GET /users/:id` - 사용자 조회
- `PUT /users/:id` - 사용자 수정
- `GET /health` - 헬스체크

### Order Service (포트 8081)
- `POST /orders` - 주문 생성
- `GET /orders/:id` - 주문 조회
- `PUT /orders/:id/status` - 주문 상태 변경
- `GET /users/:userId/orders` - 사용자별 주문 조회
- `GET /health` - 헬스체크

### Notification Service (포트 8082)
- `POST /webhook/events` - 이벤트 웹훅
- `GET /users/:userId/notifications` - 사용자 알림 조회
- `GET /health` - 헬스체크

## 🎯 Go Workspace의 주요 장점

### 1. 모듈 간 로컬 개발
- `replace` 디렉티브 없이 로컬 모듈 직접 참조
- 실시간 코드 변경 반영
- 타입 안전성 보장

### 2. 일관된 의존성 관리
- 모든 모듈이 동일한 버전 사용
- 의존성 충돌 방지
- 버전 일관성 자동 유지

### 3. 통합 개발 환경
- 하나의 워크스페이스에서 모든 관련 프로젝트 관리
- IDE에서 전체 코드베이스 탐색 가능
- 통합 리팩토링 지원

### 4. 실무 패턴 구현
- 공통 설정 관리 (`shared/config`)
- 구조화된 로깅 (`shared/logger`)
- 통합 에러 처리 (`shared/errors`)
- 공통 미들웨어 (`shared/middleware`)
- 이벤트 드리븐 아키텍처 (`shared/events`)

## 🛠️ 개발 환경 설정

### 환경 변수 설정
```bash
# env.example 파일을 참고하여 환경 변수 설정
cp env.example .env

# 또는 직접 설정
export LOG_LEVEL=debug
export LOG_FORMAT=json
export SERVER_PORT=8080
```

### IDE 설정
- **GoLand/IntelliJ**: Go workspace 자동 인식
- **VS Code**: Go extension으로 워크스페이스 지원
- **Vim/Neovim**: vim-go 플러그인으로 워크스페이스 지원

## 📚 학습 자료

- [Go Workspaces 공식 문서](https://go.dev/doc/tutorial/workspaces)
- [Go Modules Reference](https://go.dev/ref/mod)
- [Microservices with Go](https://microservices.io/patterns/microservices.html)

## 🤝 기여하기

이 예제에 개선사항이나 새로운 사용 사례가 있다면 언제든 기여해 주세요!

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 라이선스

MIT License