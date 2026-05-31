"""
04. 제어문 — 조건문과 반복문

참고: ../../01-beginner/04-control-flow.md
"""

# === if / elif / else ===
print("=== 등급 계산 ===")

def get_grade(score: int) -> str:
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    return "F"

for score in [95, 85, 73, 62, 45]:
    print(f"{score} → {get_grade(score)}")

# === for 루프 ===
print("\n=== for 루프 ===")

# range
print("1-5:", end=" ")
for i in range(1, 6):
    print(i, end=" ")
print()

# enumerate
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")

# zip
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
for name, age in zip(names, ages):
    print(f"{name}: {age}")

# === while 루프 ===
print("\n=== while 루프 ===")
count = 0
while count < 5:
    count += 1
    if count == 3:
        continue
    print(f"count = {count}")

# === FizzBuzz ===
print("\n=== FizzBuzz (1-15) ===")
for i in range(1, 16):
    if i % 15 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)

# === 별 찍기 ===
print("\n=== 피라미드 ===")
n = 5
for i in range(1, n + 1):
    print(" " * (n - i) + "*" * (2 * i - 1))

# === for-else ===
print("\n=== 소수 판별 (for-else) ===")

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

for n in range(2, 20):
    if is_prime(n):
        print(n, end=" ")
print()
