# 00. Quick Start - 10분 안에 Python 핵심 파악

> 💡 **Java/Go/Kotlin 개발자를 위한 핵심:**
> Python은 동적 타이핑 언어이지만, 타입 힌트로 정적 분석이 가능합니다.
> 들여쓰기가 블록을 정의하며, 간결함을 추구합니다.

## 🎯 학습 목표

1. Python 문법을 다른 언어와 비교하여 빠르게 이해
2. Pythonic한 코드 스타일 감 잡기
3. 핵심 기능 5가지 빠르게 훑기

## 🔄 다른 언어와 핵심 비교

### 변수 선언

| Java | Go | Kotlin | Python |
|------|-----|--------|--------|
| `String name = "Kim";` | `name := "Kim"` | `val name = "Kim"` | `name = "Kim"` |
| `int age = 30;` | `var age int = 30` | `var age: Int = 30` | `age: int = 30` |
| `final double PI = 3.14;` | `const PI = 3.14` | `const val PI = 3.14` | `PI: Final = 3.14` |

### 컬렉션

| 개념 | Java | Go | Kotlin | Python |
|------|------|-----|--------|--------|
| 리스트 | `List.of(1, 2, 3)` | `[]int{1, 2, 3}` | `listOf(1, 2, 3)` | `[1, 2, 3]` |
| 맵/딕셔너리 | `Map.of("a", 1)` | `map[string]int{"a": 1}` | `mapOf("a" to 1)` | `{"a": 1}` |
| 집합 | `Set.of(1, 2)` | 없음 (map으로 구현) | `setOf(1, 2)` | `{1, 2}` |

### 함수

| Java | Go | Kotlin | Python |
|------|-----|--------|--------|
| `int add(int a, int b)` | `func add(a, b int) int` | `fun add(a: Int, b: Int): Int` | `def add(a: int, b: int) -> int:` |

### 클래스

| Java | Kotlin | Python |
|------|--------|--------|
| `class Person { }` | `class Person { }` | `class Person:` |
| `public Person(String name)` | `class Person(val name: String)` | `def __init__(self, name: str):` |
| `person.getName()` | `person.name` | `person.name` |

### 에러 처리

| Java | Go | Python |
|------|-----|--------|
| `try { } catch (Exception e) { }` | `if err != nil { }` | `try: ... except Exception as e:` |

### Null 처리

| Java | Kotlin | Python |
|------|--------|--------|
| `Optional<String>` | `String?` | `str \| None` 또는 `Optional[str]` |
| `opt.orElse("default")` | `value ?: "default"` | `value or "default"` |

## 📚 예제 목록

| 파일 | 설명 | 난이도 | 소요시간 |
|------|------|--------|----------|
| [01_syntax_comparison.py](./01_syntax_comparison.py) | Java/Go 스타일 vs Python 스타일 | ⭐ | 5분 |
| [02_quick_tour.py](./02_quick_tour.py) | Python 핵심 기능 투어 | ⭐ | 5분 |

## 🚀 실행 방법

```bash
# 문법 비교 예제
python 01_syntax_comparison.py

# 핵심 기능 투어
python 02_quick_tour.py
```

## ⚠️ 첫날부터 알아야 할 것

1. **들여쓰기가 문법이다** - 탭과 스페이스를 섞지 마세요 (4 스페이스 권장)
2. **세미콜론 없음** - 한 줄에 여러 문장 쓸 때만 사용
3. **`self`는 명시적** - Java의 `this`와 달리 메서드에 항상 첫 번째 인자로 명시
4. **`None`은 `is`로 비교** - `if x is None:` (== 아님!)
5. **인덱스는 0부터, 슬라이싱은 끝 미포함** - `list[0:2]`는 인덱스 0, 1만

## 📖 추가 학습 자료

- [Python 공식 튜토리얼](https://docs.python.org/3/tutorial/)
- [The Zen of Python](https://peps.python.org/pep-0020/) - `import this`
- [PEP 8 스타일 가이드](https://pep8.org/)

