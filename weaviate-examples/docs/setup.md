# 환경 설정 가이드 🛠️

## 1. 필수 요구사항

### 1.1 소프트웨어
- Python 3.10 이상
- Docker Desktop (Weaviate 실행용)
- Git
- 코드 에디터 (VS Code 권장)

### 1.2 계정 (선택사항)
- OpenAI API 키 (벡터화용)
- Cohere API 키 (선택)
- Hugging Face 토큰 (선택)

## 2. Python 환경 설정

### 2.1 Python 설치 확인

```bash
python --version
# Python 3.10.0 이상이어야 함
```

Python이 설치되어 있지 않다면:
- **Windows**: [python.org](https://www.python.org/downloads/) 에서 다운로드
- **macOS**: `brew install python3`
- **Linux**: `sudo apt install python3.10`

### 2.2 가상 환경 생성

가상 환경은 **프로젝트별로 독립된 Python 환경**을 만듭니다.

```bash
# 프로젝트 디렉토리로 이동
cd weaviate-examples

# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화
# macOS/Linux:
source venv/bin/activate

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# Windows (CMD):
venv\Scripts\activate.bat
```

**활성화 확인:**
터미널 프롬프트 앞에 `(venv)`가 표시되면 성공!

```bash
(venv) user@computer:~/weaviate-examples$
```

### 2.3 의존성 설치

```bash
# requirements.txt의 모든 패키지 설치
pip install -r requirements.txt

# 설치 확인
pip list
```

## 3. Docker 설정

### 3.1 Docker Desktop 설치

- **Windows/macOS**: [Docker Desktop](https://www.docker.com/products/docker-desktop/) 다운로드 및 설치
- **Linux**:
  ```bash
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  ```

### 3.2 Docker 설치 확인

```bash
docker --version
# Docker version 24.0.0 이상

docker-compose --version
# Docker Compose version v2.20.0 이상
```

## 4. Weaviate 실행

### 4.1 Docker Compose 파일 생성

`project/docker-compose.yml` 파일이 이미 준비되어 있습니다.

```bash
cd project
cat docker-compose.yml  # 파일 내용 확인
```

### 4.2 Weaviate 시작

```bash
# Weaviate 컨테이너 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f weaviate
```

**성공 메시지 예시:**
```
weaviate  | {"level":"info","msg":"Weaviate is ready!","time":"2024-01-15T10:00:00Z"}
```

### 4.3 Weaviate 접속 확인

브라우저에서 http://localhost:8080/v1/meta 접속

정상 응답 예시:
```json
{
  "version": "1.23.0"
}
```

또는 터미널에서:
```bash
curl http://localhost:8080/v1/meta
```

### 4.4 Weaviate 중지/시작

```bash
# 중지
docker-compose down

# 시작
docker-compose up -d

# 데이터 포함 완전 삭제
docker-compose down -v
```

## 5. 환경 변수 설정

### 5.1 .env 파일 생성

```bash
# .env.example을 복사
cp .env.example .env
```

### 5.2 API 키 설정

`.env` 파일을 열어 다음 값들을 설정합니다:

```bash
# Weaviate 설정 (기본값 사용)
WEAVIATE_URL=http://localhost:8080

# OpenAI API 키 (필수)
OPENAI_API_KEY=sk-your-api-key-here

# 선택사항
COHERE_API_KEY=your-cohere-key
HUGGINGFACE_API_KEY=your-hf-key
```

### 5.3 OpenAI API 키 발급

1. https://platform.openai.com/ 접속
2. 로그인 또는 회원가입
3. 우측 상단 프로필 → "View API Keys"
4. "Create new secret key" 클릭
5. 생성된 키를 `.env` 파일에 복사

**비용:**
- text-embedding-3-small: $0.02 / 1M 토큰 (매우 저렴)
- 학습용으로 $5 충전이면 충분

## 6. 설치 확인

### 6.1 연결 테스트

```bash
cd lessons/01-basics
python 01_connection.py
```

**성공 메시지:**
```
✅ Weaviate 연결 성공!
버전: 1.23.0
준비 상태: True
```

### 6.2 문제 해결

#### Python 가상 환경 활성화 안됨
```bash
# 증상: (venv)가 표시되지 않음
# 해결: 가상 환경 재활성화
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

#### Docker 연결 실패
```bash
# 증상: Cannot connect to Docker daemon
# 해결: Docker Desktop 실행 확인
# Windows/macOS: Docker Desktop 앱 실행
# Linux: sudo systemctl start docker
```

#### Weaviate 연결 실패
```bash
# 증상: Connection refused (localhost:8080)
# 해결:
docker-compose down
docker-compose up -d
docker-compose logs -f weaviate  # 에러 확인
```

#### OpenAI API 키 오류
```bash
# 증상: Invalid API key
# 해결:
# 1. .env 파일의 키 확인
# 2. 키 앞뒤 공백 제거
# 3. 따옴표 없이 입력 (올바름: OPENAI_API_KEY=sk-xxx)
```

## 7. VS Code 설정 (권장)

### 7.1 유용한 확장 프로그램

1. **Python** (Microsoft)
2. **Pylance** (Microsoft)
3. **Docker** (Microsoft)
4. **Python Indent** (Kevin Rose)

### 7.2 VS Code 설정

`.vscode/settings.json` 생성:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "[python]": {
    "editor.rulers": [88],
    "editor.tabSize": 4
  }
}
```

## 8. 디렉토리 구조 확인

올바른 구조:

```
weaviate-examples/
├── venv/                    # 가상 환경 (생성됨)
├── .env                     # 환경 변수 (생성됨)
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── docs/
├── lessons/
├── project/
│   └── docker-compose.yml
└── utils/
```

## 9. 다음 단계

환경 설정이 완료되었습니다! 🎉

👉 [Weaviate 핵심 개념 학습](./concepts.md)

👉 [초급 학습 시작하기](../lessons/01-basics/README.md)

## 10. 참고 자료

- [Weaviate 공식 문서](https://weaviate.io/developers/weaviate)
- [Python 공식 문서](https://docs.python.org/3/)
- [Docker 공식 문서](https://docs.docker.com/)
- [OpenAI API 문서](https://platform.openai.com/docs/)
