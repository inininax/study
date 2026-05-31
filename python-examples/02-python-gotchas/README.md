# 02. Python Gotchas - ⚠️ 실수하기 쉬운 패턴

> 💡 **Java/Go/Kotlin 개발자를 위한 핵심:**
> 이 섹션은 **가장 중요한 섹션**입니다!
> 다른 언어의 습관이 Python에서 버그를 만드는 패턴들을 다룹니다.
> 실무에서 디버깅 시간을 줄이려면 반드시 읽어보세요.

## 🎯 학습 목표

1. 다른 언어 습관으로 인한 Python 함정 인식
2. 각 함정의 원인 이해
3. 올바른 해결 방법 습득

## ⚠️ 함정 목록 (중요도 순)

| 함정 | 위험도 | 설명 |
|------|--------|------|
| 가변 기본 인자 | 🔴 높음 | `def func(items=[])` 는 모든 호출이 같은 리스트 공유! |
| 클래스 변수 공유 | 🔴 높음 | 인스턴스 간 가변 클래스 변수 공유 |
| is vs == | 🟠 중간 | 작은 정수 캐싱으로 인한 혼란 |
| Late Binding Closures | 🟠 중간 | 루프 안 람다가 마지막 값만 참조 |
| 얕은 복사 | 🟠 중간 | `list[:]`와 `.copy()`는 얕은 복사! |
| 변수 스코프 누출 | 🟡 낮음 | for문 변수가 바깥에서 접근 가능 |
| 순환 참조 | 🟡 낮음 | `__del__`이 호출되지 않는 경우 |

## 📚 예제 목록

| 파일 | 설명 | 위험도 | 소요시간 |
|------|------|--------|----------|
| [01_mutable_default_args.py](./01_mutable_default_args.py) | 가변 기본 인자 함정 | 🔴 | 5분 |
| [02_class_vs_instance_vars.py](./02_class_vs_instance_vars.py) | 클래스 변수 공유 문제 | 🔴 | 5분 |
| [03_is_vs_equals.py](./03_is_vs_equals.py) | is vs == 차이 | 🟠 | 5분 |
| [04_late_binding_closures.py](./04_late_binding_closures.py) | 클로저 late binding | 🟠 | 5분 |
| [05_shallow_vs_deep_copy.py](./05_shallow_vs_deep_copy.py) | 얕은 복사 문제 | 🟠 | 5분 |
| [06_variable_scope_leaking.py](./06_variable_scope_leaking.py) | 변수 스코프 누출 | 🟡 | 5분 |
| [07_circular_reference.py](./07_circular_reference.py) | 순환 참조와 메모리 | 🟡 | 5분 |

## 🚀 실행 방법

```bash
# 모든 예제 실행
for f in *.py; do python "$f"; echo "---"; done

# 개별 실행
python 01_mutable_default_args.py
```

## 📖 추가 학습 자료

- [Python Gotchas - 공식 FAQ](https://docs.python.org/3/faq/programming.html)
- [Common Python Mistakes - StackOverflow](https://stackoverflow.com/questions/1011431/common-pitfalls-in-python)

