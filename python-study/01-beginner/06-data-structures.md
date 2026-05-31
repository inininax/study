# 06. 자료구조 (리스트/튜플/딕셔너리/셋)

## 🎯 학습 목표
- 리스트, 튜플, 딕셔너리, 셋의 차이를 안다
- 각 자료구조의 메서드를 활용할 수 있다
- 상황에 맞는 자료구조를 선택할 수 있다

## 1. 리스트 (List)

**순서가 있고 변경 가능한** 자료 모음입니다.

### 1.1 생성
```python
empty = []
numbers = [1, 2, 3, 4, 5]
mixed = [1, "Hello", 3.14, True, [1, 2]]
from_range = list(range(5))      # [0, 1, 2, 3, 4]
from_string = list("Python")     # ['P', 'y', 't', 'h', 'o', 'n']
```

### 1.2 인덱싱과 슬라이싱
```python
fruits = ["apple", "banana", "cherry", "date", "elderberry"]

# 인덱싱
print(fruits[0])     # apple
print(fruits[-1])    # elderberry (음수 인덱스)
print(fruits[-2])    # date

# 슬라이싱 [start:stop:step]
print(fruits[1:3])   # ['banana', 'cherry']
print(fruits[:3])    # ['apple', 'banana', 'cherry']
print(fruits[2:])    # ['cherry', 'date', 'elderberry']
print(fruits[::2])   # ['apple', 'cherry', 'elderberry']
print(fruits[::-1])  # 역순
```

### 1.3 주요 메서드
```python
nums = [3, 1, 4, 1, 5]

# 추가
nums.append(9)           # [3, 1, 4, 1, 5, 9]
nums.insert(0, 99)       # [99, 3, 1, 4, 1, 5, 9]
nums.extend([2, 6, 5])   # [99, 3, 1, 4, 1, 5, 9, 2, 6, 5]

# 제거
nums.remove(99)          # 첫 99 제거
last = nums.pop()        # 마지막 요소 제거 후 반환
first = nums.pop(0)      # 첫 요소 제거 후 반환
del nums[0]              # 인덱스로 삭제
nums.clear()             # 모두 제거

# 검색/카운트
nums = [3, 1, 4, 1, 5]
print(nums.index(4))     # 2 (첫 4의 인덱스)
print(nums.count(1))     # 2 (1이 나타난 횟수)
print(4 in nums)         # True

# 정렬
nums.sort()              # 오름차순
nums.sort(reverse=True)  # 내림차순
sorted_nums = sorted(nums)  # 원본 유지, 새 리스트
nums.reverse()           # 역순
```

### 1.4 리스트 연산
```python
a = [1, 2, 3]
b = [4, 5, 6]

# 연결
c = a + b                # [1, 2, 3, 4, 5, 6]

# 반복
d = a * 3                # [1, 2, 3, 1, 2, 3, 1, 2, 3]

# 길이
print(len(a))            # 3

# 최소/최대/합
print(min(a), max(a), sum(a))  # 1 3 6
```

### 1.5 리스트 컴프리헨션 (미리보기)
```python
# 1부터 10까지의 제곱
squares = [x ** 2 for x in range(1, 11)]
# [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# 짝수만 필터링
evens = [x for x in range(20) if x % 2 == 0]

# 2차원 리스트
matrix = [[i * j for j in range(5)] for i in range(5)]
```

### 1.6 리스트 복사 주의!
```python
a = [1, 2, 3]
b = a               # 참조 (같은 객체)
b.append(4)
print(a)            # [1, 2, 3, 4]  ← a도 변경됨!

# 얕은 복사
b = a.copy()        # 또는 list(a) 또는 a[:]
b = list(a)
b = a[:]

# 깊은 복사 (중첩된 객체까지)
import copy
b = copy.deepcopy(a)
```

## 2. 튜플 (Tuple)

**순서가 있고 변경 불가능한** 자료 모음입니다.

### 2.1 생성
```python
empty = ()
single = (42,)              # 콤마 필수!
not_tuple = (42)            # 그냥 정수 42
point = (10, 20)
mixed = (1, "Hello", 3.14)
tuple_from = tuple([1, 2, 3])
```

### 2.2 특징
```python
t = (1, 2, 3)
print(t[0])              # 1
print(t[-1])             # 3

# 변경 불가
# t[0] = 99              # TypeError!

# 메서드 적음
print(t.count(2))        # 1
print(t.index(3))        # 2

# 튜플도 슬라이싱 가능
print(t[1:])             # (2, 3)
```

### 2.3 언패킹
```python
point = (10, 20)
x, y = point
print(x, y)              # 10 20

# 함수의 다중 반환값
def get_min_max(nums):
    return min(nums), max(nums)

low, high = get_min_max([3, 1, 4, 1, 5])
```

### 2.4 리스트 vs 튜플
| 특성 | 리스트 | 튜플 |
|------|--------|------|
| 변경 가능 | ✅ | ❌ |
| 순서 | ✅ | ✅ |
| 메모리 | 더 큼 | 더 작음 |
| 속도 | 느림 | 빠름 |
| 해시 가능 | ❌ | ✅ |

> 💡 **언제 사용?**
> - **리스트**: 데이터가 변경될 때
> - **튜플**: 데이터가 고정될 때 (좌표, 날짜 등)

## 3. 딕셔너리 (Dictionary)

**키-값 쌍** 으로 이루어진 자료 모음입니다.

### 3.1 생성
```python
empty = {}
person = {"name": "Alice", "age": 25, "city": "Seoul"}
from_pairs = dict([("a", 1), ("b", 2)])
from_kwargs = dict(name="Bob", age=30)
```

### 3.2 접근과 수정
```python
person = {"name": "Alice", "age": 25}

# 접근
print(person["name"])              # Alice
print(person.get("name"))          # Alice
print(person.get("phone"))         # None (KeyError 없음)
print(person.get("phone", "없음")) # "없음" (기본값)

# 수정/추가
person["age"] = 26                 # 수정
person["email"] = "a@example.com"  # 추가

# 삭제
del person["age"]
phone = person.pop("phone", None)  # 안전한 삭제
person.clear()                     # 모두 제거
```

### 3.3 주요 메서드
```python
person = {"name": "Alice", "age": 25, "city": "Seoul"}

# 키, 값, 키-값 쌍 가져오기
print(list(person.keys()))    # ['name', 'age', 'city']
print(list(person.values()))  # ['Alice', 25, 'Seoul']
print(list(person.items()))   # [('name', 'Alice'), ('age', 25), ...]

# 합치기 (Python 3.5+)
defaults = {"role": "user", "active": True}
full = {**defaults, **person}

# 합치기 (Python 3.9+)
full = defaults | person       # | 연산자

# update
person.update({"age": 30, "phone": "010-1234"})

# 포함 확인
print("name" in person)        # True
print("phone" in person)       # False
```

### 3.4 순회
```python
person = {"name": "Alice", "age": 25, "city": "Seoul"}

# 키만
for key in person:
    print(key)

# 값만
for value in person.values():
    print(value)

# 키-값 모두 (가장 많이 사용)
for key, value in person.items():
    print(f"{key}: {value}")
```

### 3.5 딕셔너리 컴프리헨션
```python
squares = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# 필터링
positive = {k: v for k, v in {"a": 1, "b": -2, "c": 3}.items() if v > 0}
```

### 3.6 중첩 딕셔너리
```python
users = {
    "alice": {"age": 25, "email": "a@example.com"},
    "bob": {"age": 30, "email": "b@example.com"},
}

print(users["alice"]["age"])  # 25
users["alice"]["age"] = 26
```

## 4. 셋 (Set)

**순서 없고 중복 없는** 자료 모음입니다.

### 4.1 생성
```python
empty = set()                # ⚠️ {}는 빈 딕셔너리!
fruits = {"apple", "banana", "cherry"}
from_list = set([1, 2, 2, 3, 3, 3])  # {1, 2, 3}
unique = set("Hello")        # {'H', 'e', 'l', 'o'}
```

### 4.2 주요 메서드
```python
s = {1, 2, 3}

# 추가/제거
s.add(4)                     # {1, 2, 3, 4}
s.update([5, 6, 7])          # {1, 2, 3, 4, 5, 6, 7}
s.discard(7)                 # 없으면 무시
s.remove(6)                  # 없으면 KeyError
s.pop()                      # 임의의 요소 제거
s.clear()                    # 모두 제거
```

### 4.3 집합 연산
```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# 합집합
print(a | b)                 # {1, 2, 3, 4, 5, 6}
print(a.union(b))

# 교집합
print(a & b)                 # {3, 4}
print(a.intersection(b))

# 차집합
print(a - b)                 # {1, 2}
print(a.difference(b))

# 대칭 차집합 (XOR)
print(a ^ b)                 # {1, 2, 5, 6}
print(a.symmetric_difference(b))

# 부분집합/상위집합
print({1, 2}.issubset(a))    # True
print(a.issuperset({1, 2}))  # True
```

### 4.4 활용 예시
```python
# 중복 제거
nums = [1, 2, 2, 3, 3, 3, 4]
unique = list(set(nums))     # [1, 2, 3, 4]

# 빠른 멤버십 테스트 (리스트보다 빠름)
banned = {"hacker", "spam", "bot"}
if username in banned:       # O(1)
    print("차단된 사용자")

# 두 리스트의 공통 요소
list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]
common = list(set(list1) & set(list2))  # [3, 4]
```

### 4.5 frozenset (불변 셋)
```python
fs = frozenset([1, 2, 3])
# fs.add(4)  # AttributeError

# 딕셔너리 키나 셋의 요소로 사용 가능
d = {frozenset([1, 2]): "value"}
```

## 5. 자료구조 비교

| 자료구조 | 순서 | 변경 | 중복 | 키-값 | 용도 |
|---------|------|------|------|-------|------|
| list | ✅ | ✅ | ✅ | ❌ | 순서가 있는 데이터 |
| tuple | ✅ | ❌ | ✅ | ❌ | 고정된 데이터 (좌표) |
| dict | ✅* | ✅ | 키 ❌ | ✅ | 키로 빠른 검색 |
| set | ❌ | ✅ | ❌ | ❌ | 중복 제거, 집합 연산 |

> *Python 3.7+ 에서 dict는 입력 순서를 유지합니다.

### 시간 복잡도
| 연산 | list | dict/set | tuple |
|------|------|----------|-------|
| 검색 (`x in s`) | O(n) | O(1) | O(n) |
| 추가 | O(1) | O(1) | ❌ |
| 삭제 | O(n) | O(1) | ❌ |
| 인덱스 접근 | O(1) | O(1) | O(1) |

## 6. 실전 예제

### 예제 1: 단어 빈도 카운터
```python
text = "the quick brown fox jumps over the lazy dog the end"
words = text.split()

freq = {}
for word in words:
    freq[word] = freq.get(word, 0) + 1

print(freq)
# {'the': 3, 'quick': 1, 'brown': 1, ...}
```

### 예제 2: 학생 관리
```python
students = []

def add_student(name, age, grades):
    students.append({
        "name": name,
        "age": age,
        "grades": grades,
        "avg": sum(grades) / len(grades),
    })

add_student("Alice", 20, [85, 90, 78])
add_student("Bob", 22, [70, 75, 80])

# 평균 점수 순 정렬
sorted_students = sorted(students, key=lambda s: s["avg"], reverse=True)
for s in sorted_students:
    print(f"{s['name']}: {s['avg']:.1f}")
```

### 예제 3: 중복 제거 (순서 유지)
```python
items = ["apple", "banana", "apple", "cherry", "banana"]

# 순서 유지하며 중복 제거 (Python 3.7+)
unique = list(dict.fromkeys(items))
print(unique)  # ['apple', 'banana', 'cherry']
```

## 📝 연습 문제

### 문제 1: 리스트 평균
숫자 리스트를 받아 평균을 계산하는 함수를 작성하세요.

### 문제 2: 두 리스트 합치기 (중복 제거)
두 리스트를 받아 중복 없이 합친 정렬된 리스트를 반환하세요.

### 문제 3: 영단어 카운트
문장을 받아 각 단어의 등장 횟수를 딕셔너리로 반환하세요.

### 문제 4: 전화번호부
이름과 전화번호를 저장하고 검색/추가/삭제할 수 있는 전화번호부를 만드세요.

### 문제 5: 가장 빈도 높은 요소
리스트에서 가장 자주 등장하는 요소를 찾으세요.

## ✅ 체크리스트
- [ ] 리스트와 튜플의 차이를 안다
- [ ] 슬라이싱을 활용할 수 있다
- [ ] 딕셔너리의 키-값 구조를 안다
- [ ] 셋으로 중복을 제거할 수 있다
- [ ] 각 자료구조에 맞는 메서드를 사용할 수 있다
- [ ] 어떤 상황에 어떤 자료구조를 쓸지 안다

## 🔗 다음 챕터
👉 [07. 문자열 처리](./07-strings.md)
