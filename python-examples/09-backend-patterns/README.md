# 09. Backend Patterns - 백엔드 실무 패턴

> 💡 **핵심:**
> FastAPI + Pydantic + SQLAlchemy는 Python 백엔드의 황금 조합입니다.
> Spring Boot나 Go의 패턴과 유사하게 Clean Architecture를 적용할 수 있습니다.

## 🔄 다른 언어와 비교

| 구분 | Spring Boot | Go | FastAPI |
|------|-------------|-----|---------|
| 프레임워크 | Spring MVC | Gin, Echo | FastAPI |
| ORM | JPA/Hibernate | GORM | SQLAlchemy |
| Validation | Bean Validation | go-playground | Pydantic |
| DI | Spring DI | wire, fx | Depends |

## 📚 현재 상태

이 섹션은 로드맵 README만 있습니다. 실행 가능한 백엔드 예제는 아직 추가 전입니다.

## 🧭 확장 예정 주제

- FastAPI 기초
- Pydantic 검증
- 의존성 주입
- Repository 패턴

## 🚀 실행 방법

```bash
# 의존성 설치
pip install fastapi uvicorn pydantic sqlalchemy

# 예제 추가 후 서버 실행
uvicorn <module_name>:app --reload
```
