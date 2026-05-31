# 02. 웹 개발 (FastAPI/Flask)

## 🎯 학습 목표
- Python 웹 프레임워크를 선택할 수 있다
- FastAPI 로 REST API 를 만든다
- ORM 으로 데이터베이스를 다룬다
- 인증과 보안 기초를 안다

## 1. Python 웹 프레임워크

| 프레임워크 | 특징 | 추천 용도 |
|-----------|------|-----------|
| **FastAPI** | 빠름, 비동기, 타입 힌트, 자동 문서 | 현대적 API (권장 ✅) |
| **Flask** | 가벼움, 유연 | 작은 앱, 학습 |
| **Django** | 풀스택, 배터리 포함 | 큰 웹 앱, 어드민 필요 |
| **Starlette** | 비동기 기반 | 저수준 API |
| **Litestar** | 빠른 FastAPI 대안 | 신규 프로젝트 |

## 2. Flask 기초

### 2.1 설치 및 Hello World
```bash
pip install flask
```

```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/hello/<name>")
def hello(name):
    return f"Hello, {name}!"

if __name__ == "__main__":
    app.run(debug=True)
```

```bash
python app.py
# http://127.0.0.1:5000/
```

### 2.2 라우팅과 메서드
```python
@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        return "Create user"
    return "List users"

@app.route("/users/<int:user_id>", methods=["GET", "PUT", "DELETE"])
def user(user_id):
    ...
```

### 2.3 요청 처리
```python
from flask import request, jsonify

@app.route("/users", methods=["POST"])
def create_user():
    # JSON 요청
    data = request.get_json()
    name = data.get("name")

    # 쿼리 파라미터
    role = request.args.get("role", "user")

    # 폼 데이터
    email = request.form.get("email")

    # 헤더
    auth = request.headers.get("Authorization")

    return jsonify({"name": name, "role": role}), 201
```

### 2.4 템플릿 (Jinja2)
```python
from flask import render_template

@app.route("/")
def home():
    return render_template("index.html", name="Alice")
```

```html
<!-- templates/index.html -->
<h1>Hello, {{ name }}!</h1>
<ul>
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}
</ul>
```

## 3. FastAPI (권장 ✅)

### 3.1 설치 및 시작
```bash
pip install fastapi uvicorn[standard]
```

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello"}

@app.get("/items/{item_id}")
def get_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

```bash
uvicorn main:app --reload
# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs   ← 자동 Swagger UI!
# http://127.0.0.1:8000/redoc  ← ReDoc
```

### 3.2 Pydantic 모델
```python
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=0, le=150)
    role: str = "user"

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    # 자동 검증, JSON 파싱, 응답 직렬화!
    new_user = {"id": 1, **user.model_dump()}
    return new_user
```

### 3.3 비동기 핸들러
```python
import asyncio
import httpx

@app.get("/external")
async def fetch_external():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com")
        return response.json()
```

### 3.4 의존성 주입
```python
from fastapi import Depends, Header, HTTPException

def get_db():
    db = create_db_session()
    try:
        yield db
    finally:
        db.close()

def verify_token(token: str = Header(...)):
    if token != "secret":
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

@app.get("/users/me", dependencies=[Depends(verify_token)])
def get_me(db = Depends(get_db)):
    return db.query("...").first()
```

### 3.5 예외 처리
```python
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)},
    )

@app.get("/users/{id}")
def get_user(id: int):
    if id < 0:
        raise HTTPException(status_code=400, detail="잘못된 ID")
    if id > 1000:
        raise HTTPException(status_code=404, detail="없음")
    return {"id": id}
```

### 3.6 라우터 분리
```python
# routers/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def list_users():
    return []

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"id": user_id}

# main.py
from routers import users
app.include_router(users.router)
```

## 4. 데이터베이스 (SQLAlchemy)

### 4.1 설치
```bash
pip install sqlalchemy alembic psycopg2-binary  # PostgreSQL
```

### 4.2 모델 정의
```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey
from typing import List

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)

    posts: Mapped[List["Post"]] = relationship(back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    author: Mapped["User"] = relationship(back_populates="posts")
```

### 4.3 세션과 쿼리
```python
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://user:pass@localhost/db")
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

# 사용
with SessionLocal() as session:
    # Create
    user = User(name="Alice", email="a@example.com")
    session.add(user)
    session.commit()

    # Read
    user = session.get(User, 1)
    all_users = session.scalars(select(User)).all()

    # Filter
    alice = session.scalars(
        select(User).where(User.name == "Alice")
    ).first()

    # Update
    user.name = "Alicia"
    session.commit()

    # Delete
    session.delete(user)
    session.commit()
```

### 4.4 FastAPI 와 통합
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def create_user(user: UserCreate, db = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

## 5. 인증과 보안

### 5.1 비밀번호 해싱
```bash
pip install passlib[bcrypt]
```

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 회원가입 시
hashed = pwd_context.hash("plain_password")

# 로그인 시
if pwd_context.verify("plain_password", hashed):
    print("OK")
```

### 5.2 JWT 토큰
```bash
pip install python-jose[cryptography]
```

```python
from jose import jwt
from datetime import datetime, timedelta

SECRET = "your-secret-key"
ALGORITHM = "HS256"

def create_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None

# 사용
token = create_token({"sub": "alice", "role": "admin"})
data = verify_token(token)
```

### 5.3 OAuth2 + FastAPI
```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(401, "Invalid token")
    return payload

@app.get("/me")
def read_me(user = Depends(get_current_user)):
    return user
```

### 5.4 CORS
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 5.5 보안 체크리스트
- [ ] HTTPS 사용
- [ ] 비밀번호는 항상 해싱
- [ ] SQL injection 방지 (ORM 사용)
- [ ] XSS 방지 (템플릿 자동 이스케이프)
- [ ] CSRF 토큰
- [ ] Rate limiting
- [ ] 입력 검증 (Pydantic)
- [ ] 비밀 키는 환경 변수
- [ ] 의존성 보안 업데이트 (Dependabot)

## 6. 환경 설정

### 6.1 환경 변수 (pydantic-settings)
```bash
pip install pydantic-settings
```

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```

```env
# .env
DATABASE_URL=postgresql://localhost/mydb
SECRET_KEY=supersecret
DEBUG=true
```

## 7. 비동기 데이터베이스 (asyncpg/SQLAlchemy)

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/users/")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()
```

## 8. 백그라운드 작업

### 8.1 FastAPI BackgroundTasks
```python
from fastapi import BackgroundTasks

def send_email(email: str, subject: str):
    # 실제 이메일 전송
    print(f"Sending to {email}")

@app.post("/notify")
async def notify(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email, "환영합니다")
    return {"message": "이메일이 곧 발송됩니다"}
```

### 8.2 Celery (큰 작업)
```bash
pip install celery redis
```

```python
# tasks.py
from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379")

@app.task
def heavy_task(x, y):
    return x + y

# 호출 (비동기)
result = heavy_task.delay(1, 2)
print(result.get())  # 3
```

## 9. 테스트

### 9.1 FastAPI TestClient
```python
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}

def test_create_user():
    response = client.post(
        "/users",
        json={"name": "Alice", "email": "a@x.com", "age": 25}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Alice"
```

### 9.2 비동기 테스트
```bash
pip install pytest-asyncio httpx
```

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_async():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
```

## 10. 배포

### 10.1 Gunicorn + Uvicorn
```bash
pip install gunicorn

gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 10.2 Docker
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 10.3 docker-compose.yml
```yaml
version: "3.9"
services:
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://user:pass@db/myapp

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: myapp
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

## 11. 완전한 예제: Todo API

```python
# main.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

app = FastAPI(title="Todo API", version="1.0")

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class Todo(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    done: bool = False
    created_at: datetime

# in-memory store (실제론 DB 사용)
todos: dict[str, Todo] = {}

@app.get("/todos", response_model=list[Todo])
def list_todos(done: bool | None = None):
    items = list(todos.values())
    if done is not None:
        items = [t for t in items if t.done == done]
    return items

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(404, "찾을 수 없음")
    return todos[todo_id]

@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(data: TodoCreate):
    todo = Todo(
        id=str(uuid.uuid4()),
        title=data.title,
        description=data.description,
        created_at=datetime.now(),
    )
    todos[todo.id] = todo
    return todo

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: str, data: TodoCreate):
    if todo_id not in todos:
        raise HTTPException(404, "찾을 수 없음")
    todos[todo_id].title = data.title
    todos[todo_id].description = data.description
    return todos[todo_id]

@app.patch("/todos/{todo_id}/done")
def toggle_done(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(404, "찾을 수 없음")
    todos[todo_id].done = not todos[todo_id].done
    return todos[todo_id]

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(404, "찾을 수 없음")
    del todos[todo_id]
```

## 📝 연습 문제

### 문제 1: Hello FastAPI
간단한 GET 엔드포인트 3개를 만드세요.

### 문제 2: Pydantic 모델
사용자 생성/조회 API 를 Pydantic 모델과 함께 구현하세요.

### 문제 3: 인증
JWT 토큰 기반 로그인 시스템을 만드세요.

### 문제 4: DB 연동
SQLAlchemy 로 사용자 정보를 DB 에 저장하는 API 를 만드세요.

### 문제 5: 완전한 CRUD
Todo CRUD API 를 완성하고 테스트를 작성하세요.

## ✅ 체크리스트
- [ ] FastAPI 의 기본을 안다
- [ ] Pydantic 모델로 검증한다
- [ ] 비동기 핸들러를 작성한다
- [ ] 의존성 주입을 활용한다
- [ ] SQLAlchemy 로 DB 를 다룬다
- [ ] 인증 시스템을 구현한다

## 🔗 다음 챕터
👉 [03. 데이터 분석 (NumPy/Pandas)](./03-data-analysis.md)
