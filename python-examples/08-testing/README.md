# 08. Testing - pytest 테스팅

> 💡 **핵심:**
> pytest는 Python의 사실상 표준 테스트 프레임워크입니다.
> 간결한 문법, 강력한 fixture, 풍부한 플러그인을 제공합니다.

## 🔄 다른 언어와 비교

| 구분 | Java | Go | Python |
|------|------|-----|--------|
| 기본 프레임워크 | JUnit | testing | pytest |
| Assertion | assertEquals | t.Equal | assert |
| Mock | Mockito | testify | pytest-mock |
| Fixture | @BeforeEach | - | @pytest.fixture |

## 📚 현재 상태

이 섹션은 로드맵 README만 있습니다. 실행 가능한 pytest 예제는 아직 추가 전입니다.

## 🧭 확장 예정 주제

- pytest 기초
- Fixture 활용
- Mock 사용법
- 파라미터화 테스트

## 🚀 실행 방법

```bash
# pytest 설치
pip install pytest pytest-asyncio

# 예제 추가 후 테스트 실행
pytest -v
```
