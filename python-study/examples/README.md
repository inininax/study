# 📂 예제 코드

각 단계별 학습 내용을 실제로 동작하는 코드로 정리한 폴더입니다.

## 구조
```
examples/
├── 01-beginner/        # 초급 예제
├── 02-intermediate/    # 중급 예제
├── 03-advanced/        # 고급 예제
└── 04-expert/          # 전문가 예제
```

## 실행 방법

### 1. 가상 환경 만들기
```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# 또는 venv\Scripts\activate  # Windows
```

### 2. 예제 실행
```bash
# 단일 파일
python3 01-beginner/hello.py

# 모든 예제 (Bash)
for f in 01-beginner/*.py; do
    echo "=== $f ==="
    python3 "$f"
done
```

## 권장 학습 순서

1. **README 의 챕터** 읽기
2. **예제 코드** 직접 타이핑하며 실행
3. **연습 문제** (`../exercises/`) 풀기
4. 자신의 변형 만들기

## 📝 예제 코드 작성 팁

- 각 파일의 첫 줄에 챕터 참조 주석
- 한 파일은 한 가지 개념만
- 결과 확인용 `print()` 또는 `assert`
- 설명 주석 적극 활용

```python
# 02-variables-and-types.md
# 변수와 데이터 타입 예제

# 변수 선언
name = "Alice"
age = 25

# 타입 확인
print(type(name))  # <class 'str'>
print(type(age))   # <class 'int'>

# 검증
assert isinstance(name, str)
assert isinstance(age, int)
```
