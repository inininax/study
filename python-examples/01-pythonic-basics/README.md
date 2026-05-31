# 01. Pythonic Basics - Python다운 기초

> 💡 **Java/Go/Kotlin 개발자를 위한 핵심:**
> Python에는 "Pythonic"이라는 개념이 있습니다. 이는 Python 커뮤니티에서 
> 권장하는 코드 스타일로, 간결하고 명확하며 Python의 철학을 따르는 코드입니다.
> 
> `import this`를 실행해 보세요 - The Zen of Python이 출력됩니다.

## 🎯 학습 목표

1. 동적 타이핑과 정적 타이핑의 차이 이해
2. Python 컬렉션과 Java/Go 컬렉션 비교
3. 일급 함수 개념 습득
4. Comprehension 문법 마스터
5. Unpacking 활용법 숙지

## 🔄 다른 언어와 비교

| 개념 | Java | Go | Python |
|------|------|-----|--------|
| 타이핑 | 정적/강타입 | 정적/강타입 | 동적/강타입 |
| 변수 재할당 | 같은 타입만 | 같은 타입만 | 아무 타입 |
| Null 값 | null | nil (제로값) | None |
| 함수 | 메서드 (일급 아님) | 일급 함수 | 일급 함수 |
| 컬렉션 | Generic 필수 | 타입 명시 | 동적 타입 |

## 📚 예제 목록

| 파일 | 설명 | 난이도 | 소요시간 |
|------|------|--------|----------|
| [01_variables_and_types.py](./01_variables_and_types.py) | 동적 타이핑 vs 정적 타이핑 | ⭐ | 5분 |
| [02_collections_comparison.py](./02_collections_comparison.py) | List/Dict/Set 비교 | ⭐ | 10분 |
| [03_functions_as_objects.py](./03_functions_as_objects.py) | 일급 함수 | ⭐⭐ | 10분 |
| [04_comprehensions.py](./04_comprehensions.py) | Comprehension 심화 | ⭐⭐ | 10분 |
| [05_unpacking_magic.py](./05_unpacking_magic.py) | *args, **kwargs, Unpacking | ⭐⭐ | 10분 |

## ⚠️ 이 섹션에서 다루는 Pythonic 패턴

- [ ] 동적 타이핑의 장단점
- [ ] 덕 타이핑(Duck Typing) 이해
- [ ] EAFP vs LBYL
- [ ] List Comprehension vs map/filter
- [ ] 다중 반환값 활용

## 🚀 실행 방법

```bash
# 전체 예제 실행
for f in *.py; do python "$f"; echo "---"; done

# 개별 실행
python 01_variables_and_types.py
```

## 📖 추가 학습 자료

- [The Zen of Python (PEP 20)](https://peps.python.org/pep-0020/)
- [Python Data Model](https://docs.python.org/3/reference/datamodel.html)
- [Python Glossary](https://docs.python.org/3/glossary.html)

