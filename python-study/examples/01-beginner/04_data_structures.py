"""
06. 자료구조 — 리스트/튜플/딕셔너리/셋

참고: ../../01-beginner/06-data-structures.md
"""

# === 리스트 ===
print("=== 리스트 ===")
fruits = ["apple", "banana", "cherry"]
fruits.append("date")
fruits.insert(0, "elderberry")
print(f"리스트: {fruits}")

# 슬라이싱
print(f"처음 2개: {fruits[:2]}")
print(f"마지막 2개: {fruits[-2:]}")
print(f"역순: {fruits[::-1]}")

# 컴프리헨션
squares = [x ** 2 for x in range(1, 6)]
print(f"제곱: {squares}")

# === 튜플 ===
print("\n=== 튜플 ===")
point = (3, 4)
x, y = point   # 언패킹
print(f"점: ({x}, {y})")

# 튜플은 불변
# point[0] = 10  # TypeError!

# === 딕셔너리 ===
print("\n=== 딕셔너리 ===")
person = {
    "name": "Alice",
    "age": 25,
    "city": "Seoul",
}

# 접근
print(f"이름: {person['name']}")
print(f"연락처: {person.get('phone', '없음')}")

# 순회
for key, value in person.items():
    print(f"  {key}: {value}")

# 컴프리헨션
square_map = {x: x ** 2 for x in range(1, 6)}
print(f"제곱 맵: {square_map}")

# === 셋 ===
print("\n=== 셋 ===")
fruits_set = {"apple", "banana", "cherry"}
fruits_set.add("date")
fruits_set.add("apple")  # 중복 무시
print(f"셋: {fruits_set}")

# 집합 연산
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(f"합집합: {a | b}")
print(f"교집합: {a & b}")
print(f"차집합: {a - b}")

# 중복 제거
nums = [1, 2, 2, 3, 3, 3, 4]
unique = list(set(nums))
print(f"중복 제거: {unique}")

# === 단어 빈도 ===
print("\n=== 단어 빈도 ===")
text = "the quick brown fox jumps over the lazy dog the end"
words = text.split()

freq = {}
for word in words:
    freq[word] = freq.get(word, 0) + 1

# 또는 Counter 사용
from collections import Counter
counter = Counter(words)
print(f"Top 3: {counter.most_common(3)}")
