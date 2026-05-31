# 초급 학습: Weaviate 기초 🌱

## 학습 목표

1. Weaviate 클라이언트 연결 및 설정
2. 스키마(컬렉션) 생성 및 관리
3. 기본 CRUD 작업 (생성, 읽기, 수정, 삭제)
4. 배치 작업으로 대량 데이터 처리

## 학습 순서

### 1️⃣ 연결 (`01_connection.py`)
**학습 시간: 30분**

- Weaviate 클라이언트 초기화
- 연결 상태 확인
- 메타데이터 조회
- 컨텍스트 매니저 패턴 학습

**핵심 개념:**
- 클라이언트 연결 패턴
- 리소스 관리 (try-finally)
- 환경 변수 사용

### 2️⃣ 스키마 (`02_schema.py`)
**학습 시간: 1시간**

- 컬렉션(클래스) 정의
- 속성(Properties) 설정
- 벡터화 설정
- 스키마 조회 및 삭제

**핵심 개념:**
- 데이터 타입 이해
- 벡터화 전략
- 인덱스 설정

### 3️⃣ CRUD 작업 (`03_crud.py`)
**학습 시간: 1.5시간**

- Create: 객체 생성
- Read: 객체 조회
- Update: 객체 수정
- Delete: 객체 삭제

**핵심 개념:**
- UUID 관리
- 데이터 검증
- 에러 핸들링

### 4️⃣ 배치 작업 (`04_batch_operations.py`)
**학습 시간: 1시간**

- 배치 삽입
- 성능 최적화
- 에러 처리
- 진행 상황 모니터링

**핵심 개념:**
- 배치 처리 패턴
- 성능 최적화
- 대량 데이터 처리

## 실습 방법

### 1. Weaviate 실행 확인

```bash
# Docker 컨테이너 상태 확인
docker ps | grep weaviate

# Weaviate 접속 테스트
curl http://localhost:8080/v1/meta
```

### 2. 학습 모듈 실행

```bash
# 초급 디렉토리로 이동
cd lessons/01-basics

# 각 파일을 순서대로 실행
python 01_connection.py
python 02_schema.py
python 03_crud.py
python 04_batch_operations.py
```

### 3. 코드 이해하기

각 파일을 열어서:
1. **주석 읽기**: 모든 코드에 상세한 한글 주석이 있습니다
2. **실행**: 코드를 실행하고 결과를 확인합니다
3. **수정**: 값을 바꿔가며 실험해봅니다
4. **질문**: 이해되지 않는 부분을 찾아봅니다

## Python 초보자를 위한 팁

### 타입 힌트 이해하기

```python
def create_article(title: str, content: str) -> dict:
    """
    title: str  <- 문자열 타입
    content: str <- 문자열 타입
    -> dict     <- 반환값은 딕셔너리 타입
    """
    pass
```

### 컨텍스트 매니저 패턴

```python
# 나쁜 예: 연결을 닫지 않을 수 있음
client = weaviate.connect_to_local()
# 작업 수행
client.close()  # 에러 발생시 실행 안됨!

# 좋은 예: 항상 연결을 닫음
with weaviate.connect_to_local() as client:
    # 작업 수행
    pass
# 자동으로 client.close() 호출됨
```

### 딕셔너리 vs 객체

```python
# 딕셔너리 (Python의 JSON)
article = {
    "title": "제목",
    "content": "내용"
}
print(article["title"])  # 대괄호로 접근

# 객체 (클래스 인스턴스)
class Article:
    def __init__(self, title, content):
        self.title = title
        self.content = content

article = Article("제목", "내용")
print(article.title)  # 점(.)으로 접근
```

### f-string 사용법

```python
name = "홍길동"
age = 30

# 오래된 방법
print("이름: " + name + ", 나이: " + str(age))

# 현대적 방법 (f-string)
print(f"이름: {name}, 나이: {age}")

# 표현식도 가능
print(f"10년 후: {age + 10}세")
```

## 자주 발생하는 오류

### 1. 연결 오류
```
Error: Cannot connect to Weaviate at http://localhost:8080
```
**해결:** Docker에서 Weaviate가 실행 중인지 확인
```bash
docker-compose up -d
```

### 2. 컬렉션 이미 존재
```
Error: Collection 'Article' already exists
```
**해결:** 기존 컬렉션 삭제 후 재생성
```python
client.collections.delete("Article")
```

### 3. 환경 변수 없음
```
Error: OPENAI_API_KEY not found
```
**해결:** `.env` 파일 확인 및 API 키 설정

### 4. 타입 오류
```
TypeError: expected str, got int
```
**해결:** 올바른 데이터 타입 사용
```python
# 잘못됨
{"published": 2024}

# 올바름
{"published": "2024-01-15T10:00:00Z"}
```

## 체크리스트

완료한 항목에 체크하세요:

- [ ] `01_connection.py` 실행 성공
- [ ] `02_schema.py` 실행 성공
- [ ] `03_crud.py` 실행 성공
- [ ] `04_batch_operations.py` 실행 성공
- [ ] 모든 주석 읽고 이해함
- [ ] 코드를 수정해보고 실험함
- [ ] 에러 메시지를 읽고 해결할 수 있음

## 다음 단계

초급 과정을 완료했다면:

👉 [중급 학습: 벡터 검색과 필터링](../02-intermediate/README.md)

## 참고 자료

- [Weaviate Python Client 문서](https://weaviate.io/developers/weaviate/client-libraries/python)
- [스키마 설정 가이드](https://weaviate.io/developers/weaviate/manage-data/collections)
