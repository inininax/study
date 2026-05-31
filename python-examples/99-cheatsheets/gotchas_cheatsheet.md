# Python 함정(Gotchas) 치트시트

## 🔴 가변 기본 인자

```python
# ❌ 잘못된 패턴
def add_item(item, items=[]):
    items.append(item)
    return items

add_item("a")  # ['a']
add_item("b")  # ['a', 'b'] - 같은 리스트!

# ✅ 올바른 패턴
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

## 🔴 클래스 변수 공유

```python
# ❌ 잘못된 패턴
class User:
    tags = []  # 클래스 변수 - 모든 인스턴스 공유!

# ✅ 올바른 패턴
class User:
    def __init__(self):
        self.tags = []  # 인스턴스 변수
```

## 🟠 is vs ==

```python
# is: 객체 동일성 (같은 메모리)
# ==: 값 동등성

# ✅ None 비교는 is
if value is None:
    pass

# ✅ 값 비교는 ==
if a == b:
    pass

# ⚠️ 주의: 정수 캐싱 (-5 ~ 256)
a = 100
b = 100
a is b  # True (캐싱!)

x = 1000
y = 1000
x is y  # False (캐싱 범위 밖)
```

## 🟠 Late Binding Closures

```python
# ❌ 잘못된 패턴
funcs = []
for i in range(5):
    funcs.append(lambda: i)
[f() for f in funcs]  # [4, 4, 4, 4, 4]

# ✅ 해결책: 기본 인자
funcs = []
for i in range(5):
    funcs.append(lambda x=i: x)
[f() for f in funcs]  # [0, 1, 2, 3, 4]
```

## 🟠 얕은 복사 vs 깊은 복사

```python
import copy

# 얕은 복사 (중첩 객체는 참조 공유)
shallow = original.copy()
shallow = list(original)
shallow = original[:]

# 깊은 복사 (모든 중첩 객체 복사)
deep = copy.deepcopy(original)

# ⚠️ 중첩 리스트 주의
nested = [[1, 2], [3, 4]]
shallow = nested.copy()
shallow[0].append(999)
# nested도 영향받음!
```

## 🟡 변수 스코프 누출

```python
# Python에는 블록 스코프가 없음!
for i in range(5):
    x = i * 2

print(i)  # 4 - 접근 가능!
print(x)  # 8 - 접근 가능!

# ✅ Comprehension은 자체 스코프 (Python 3+)
[y for y in range(5)]
# y는 접근 불가
```

## 🟡 순환 참조

```python
# ❌ 순환 참조 발생
class Node:
    def __init__(self):
        self.partner = None

a = Node()
b = Node()
a.partner = b
b.partner = a  # 순환!

# ✅ weakref로 해결
import weakref

class Node:
    def __init__(self):
        self.partner = None
    
    def set_partner(self, other):
        self.partner = weakref.ref(other)
```

## 요약 표

| 함정 | 원인 | 해결책 |
|------|------|--------|
| 가변 기본 인자 | 정의 시 한 번만 평가 | None 기본값 사용 |
| 클래스 변수 공유 | 클래스 레벨 선언 | __init__에서 초기화 |
| is vs == | 정수/문자열 캐싱 | 값 비교는 == 사용 |
| Late Binding | 변수 참조 지연 | 기본 인자로 캡처 |
| 얕은 복사 | 참조만 복사 | deepcopy 사용 |
| 스코프 누출 | 블록 스코프 없음 | 변수명 주의 |
| 순환 참조 | 상호 참조 | weakref 사용 |

