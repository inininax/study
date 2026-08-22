# 🚀 빠른 시작 가이드

## 5분 안에 Milvus 시작하기

### 1️⃣ 환경 설정 (2분)

```bash
# 1. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 환경변수 설정
cp .env.example .env
# 필요시 .env 파일 수정

# 4. 로그 디렉토리 생성
mkdir -p logs
```

### 2️⃣ Milvus 시작 (2분)

```bash
# Docker Compose로 Milvus 시작
docker compose up -d

# 상태 확인
docker compose ps

# 로그 확인 (optional)
docker compose logs -f milvus
```

**예상 출력**:
```
NAME                    STATUS
milvus-standalone       running
milvus-etcd            running
milvus-minio           running
milvus-redis           running
```

### 3️⃣ 첫 번째 예제 실행 (1분)

```bash
# Level 1 시작
cd level_1_basics

# 연결 테스트
python 01_connection_setup.py --mode single

# Collection 데모
python 02_collection_management.py --action demo
```

**성공 메시지**:
```
✓ Connection established
✓ Collection 'demo_simple' created successfully
```

---

## 📚 다음 단계

### Level 1 학습 시작

```bash
cd level_1_basics

# 1. 연결 관리
python 01_connection_setup.py --mode all

# 2. Collection 생성
python 02_collection_management.py --action create --name my_collection

# 3. 데이터 삽입
python 03_data_insertion.py --size small

# 4. 검색
python 04_basic_search.py --topk 10
```

### 데이터 확인

```bash
# Milvus Web UI (Attu) - Optional
# http://localhost:3000

# MinIO Console
# http://localhost:9001 (admin/minioadmin)

# Grafana (모니터링)
# http://localhost:3000 (admin/admin)
```

---

## 🔧 문제 해결

### Milvus 연결 실패

```bash
# Milvus 상태 확인
docker compose ps

# Milvus 재시작
docker compose restart milvus

# 전체 재시작
docker compose down
docker compose up -d
```

### 포트 충돌

```bash
# 사용 중인 포트 확인
netstat -an | grep 19530  # Milvus
netstat -an | grep 6379   # Redis
netstat -an | grep 9000   # MinIO

# docker-compose.yml에서 포트 변경 가능
```

### 디스크 공간 부족

```bash
# Docker 정리
docker system prune -a

# Milvus 볼륨 정리
docker compose down -v
```

---

## 📖 학습 로드맵

```
Week 1-2: Level 1 (기초)
  → Connection, Collection, Insert, Search

Week 3-4: Level 2 (중급)
  → Advanced Search, Partitions, Index Optimization

Week 5-6: Level 3 (고급)
  → Performance, Monitoring, High Availability

Week 7-10: Level 4 (실전)
  → Production Projects
```

---

## 💡 유용한 명령어

```bash
# 전체 테스트 실행
pytest

# 특정 레벨 테스트
pytest level_1_basics/tests/

# 코드 포맷팅
black .

# 타입 체크
mypy .

# 프로젝트 상태 확인
python -c "from config.settings import settings; print(settings)"
```

---

## 🆘 도움말

문제가 발생하면:
1. [문제 해결 가이드](./README.md#문제-해결) 확인
2. Milvus 로그 확인: `docker compose logs milvus`
3. 이슈 등록: GitHub Issues

**Happy Learning! 🎉**
