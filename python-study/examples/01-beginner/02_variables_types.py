"""
02. 변수와 데이터 타입

참고: ../../01-beginner/02-variables-and-types.md
"""

# === 기본 타입 ===
# int
age = 25
print(f"age = {age}, type = {type(age).__name__}")

# float
height = 175.5
print(f"height = {height}, type = {type(height).__name__}")

# str
name = "Alice"
print(f"name = {name}, type = {type(name).__name__}")

# bool
is_active = True
print(f"is_active = {is_active}, type = {type(is_active).__name__}")

# None
nothing = None
print(f"nothing = {nothing}, type = {type(nothing).__name__}")

# === 타입 변환 ===
print("\n=== 타입 변환 ===")

# 문자열 → 정수
num_str = "100"
num_int = int(num_str)
print(f"'{num_str}' → {num_int}")

# 정수 → 문자열
n = 42
s = str(n)
print(f"{n} → '{s}'")

# 실수 → 정수 (버림)
f = 3.7
i = int(f)
print(f"{f} → {i}")

# === 다중 할당 ===
print("\n=== 다중 할당 ===")
x = y = z = 0
print(f"x={x}, y={y}, z={z}")

a, b, c = 1, 2, 3
print(f"a={a}, b={b}, c={c}")

# 교환
a, b = b, a
print(f"교환 후: a={a}, b={b}")

# 언패킹
first, *rest = [1, 2, 3, 4, 5]
print(f"first={first}, rest={rest}")

# === 검증 ===
assert isinstance(age, int)
assert isinstance(name, str)
assert isinstance(height, float)
assert nothing is None
print("\n모든 검증 통과!")
