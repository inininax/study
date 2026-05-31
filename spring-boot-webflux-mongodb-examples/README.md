# Spring Boot MongoDB Reactive Examples

실무 환경 수준의 Kotlin, Spring Boot WebFlux, MongoDB Reactive를 사용한 REST API 예제 프로젝트입니다.

## 🚀 기술 스택

- **Kotlin**: 1.9.21
- **Java**: 17 (LTS)
- **Spring Boot**: 3.2.0
- **Spring WebFlux**: Reactive Web Framework
- **MongoDB Reactive**: Reactive MongoDB Driver
- **Kotlin Coroutines**: 비동기 처리
- **SpringDoc OpenAPI**: API 문서화
- **Gradle**: Build Tool

## 🛠 주요 기능

### User Management API
- 사용자 생성, 조회, 수정, 삭제 (CRUD)
- 이메일 중복 검증
- 부서별 사용자 조회
- 나이 범위별 사용자 검색
- 사용자 활성화/비활성화

### Product Management API
- 상품 생성, 조회, 수정, 삭제 (CRUD)
- 페이지네이션 지원
- 카테고리별 상품 조회
- 가격 범위별 상품 검색
- 태그 기반 상품 검색
- 재고 관리

### 기술적 특징
- **Kotlin Coroutines**: 완전한 비동기 처리
- **Reactive Streams**: Non-blocking I/O
- **MongoDB Reactive**: Reactive Database 연동
- **Global Exception Handling**: 통합 예외 처리
- **Bean Validation**: 요청 데이터 검증
- **API Documentation**: Swagger UI 제공

## 📁 프로젝트 구조

```
src/
├── main/
│   ├── kotlin/com/example/reactive/
│   │   ├── config/                  # 설정 클래스
│   │   ├── controller/              # REST Controllers
│   │   ├── dto/                     # Data Transfer Objects
│   │   ├── exception/               # 예외 처리
│   │   ├── model/                   # Domain Models
│   │   ├── repository/              # Repository Layer
│   │   ├── service/                 # Service Layer
│   │   └── ReactiveApplication.kt
│   └── resources/
│       └── application.yml
└── test/
    └── kotlin/com/example/reactive/
```

## 🚀 실행 방법

### 1. 환경 요구사항
- Java 17 이상
- MongoDB 실행 중 (기본: localhost:27017)

### 2. 애플리케이션 실행
```bash
# 프로젝트 클론 후
./gradlew bootRun
```

### 3. API 문서 확인
- Swagger UI: http://localhost:8080/swagger-ui.html
- API Docs: http://localhost:8080/api-docs

## 📚 API 엔드포인트

### User API
```
POST   /api/v1/users                               # 사용자 생성
GET    /api/v1/users                               # 전체 사용자 조회
GET    /api/v1/users/{id}                          # 사용자 조회
PUT    /api/v1/users/{id}                          # 사용자 수정
DELETE /api/v1/users/{id}                          # 사용자 삭제
GET    /api/v1/users/email/{email}                 # 이메일로 사용자 조회
GET    /api/v1/users/active                        # 활성 사용자 조회
GET    /api/v1/users/department/{dept}             # 부서별 사용자 조회
GET    /api/v1/users/search?name=xxx               # 이름 검색
GET    /api/v1/users/age-range?minAge=20&maxAge=30 # 나이 범위 검색
```

### Product API
```
POST   /api/v1/products                 # 상품 생성
GET    /api/v1/products                 # 전체 상품 조회 (페이징)
GET    /api/v1/products/{id}            # 상품 조회
PUT    /api/v1/products/{id}            # 상품 수정
DELETE /api/v1/products/{id}            # 상품 삭제
GET    /api/v1/products/search?name=xxx # 상품 검색
GET    /api/v1/products/category/{cat}  # 카테고리별 상품
GET    /api/v1/products/available       # 재고 있는 상품
GET    /api/v1/products/price-range     # 가격 범위 검색
GET    /api/v1/products/tags            # 태그 기반 검색
PATCH  /api/v1/products/{id}/stock      # 재고 수량 업데이트
```

## 🔧 설정

### MongoDB 연결 설정
```yaml
spring:
  data:
    mongodb:
      host: localhost
      port: 27017
      database: reactive_db
```

### 프로파일별 설정
- **default**: 개발 환경
- **test**: 테스트 환경
- **prod**: 운영 환경

## ✅ Kotlin Coroutines 지원

이 프로젝트는 완전한 Kotlin Coroutines 지원을 제공합니다:

- **Service Layer**: `suspend` 함수와 `Flow` 사용
- **Controller Layer**: Reactive 반환 타입 지원
- **Repository Layer**: Reactive MongoDB Repository
- **비동기 처리**: Non-blocking I/O 완전 지원

### Coroutines 사용 예시
```kotlin
// Service Layer
suspend fun createUser(request: CreateUserRequest): UserResponse {
    val user = userRepository.save(newUser).awaitFirst()
    return mapToUserResponse(user)
}

// Controller Layer
@PostMapping
suspend fun createUser(@RequestBody request: CreateUserRequest): UserResponse {
    return userService.createUser(request)
}
```

## 🧪 테스트

```bash
# 단위 테스트 실행
./gradlew test

# 통합 테스트 실행
./gradlew integrationTest
```

## 📋 TODO

- [ ] 인증/인가 (JWT) 추가
- [ ] Redis 캐시 연동
- [ ] 메트릭 및 모니터링
- [ ] Docker 컨테이너화
- [ ] CI/CD 파이프라인