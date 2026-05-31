"""
초급 연습 문제 — 정답 예시

먼저 스스로 풀어본 후 참고하세요!
"""

from typing import Any

# === 문제 4.1: FizzBuzz ===
def fizzbuzz(n: int = 100) -> None:
    for i in range(1, n + 1):
        if i % 15 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)


# === 문제 4.3: 별 찍기 (피라미드) ===
def pyramid(n: int) -> None:
    for i in range(1, n + 1):
        print(" " * (n - i) + "*" * (2 * i - 1))


# === 문제 4.4: 소수 찾기 ===
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def primes_up_to(n: int) -> list[int]:
    return [x for x in range(2, n + 1) if is_prime(x)]


# === 문제 5.1: 두 수 사이의 합 ===
def sum_between(a: int, b: int) -> int:
    if a > b:
        a, b = b, a
    return sum(range(a, b + 1))


# === 문제 5.2: 팩토리얼 ===
def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("음수 불가")
    if n <= 1:
        return 1
    return n * factorial(n - 1)


# === 문제 5.3: 회문 판별 ===
def is_palindrome(s: str) -> bool:
    s = s.lower().replace(" ", "")
    return s == s[::-1]


# === 문제 5.4: 가변 인자 평균 ===
def average(*numbers: float) -> float:
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)


# === 문제 5.5: 최대값 (max 없이) ===
def my_max(*numbers: float) -> float:
    if not numbers:
        raise ValueError("최소 1개 필요")
    result = numbers[0]
    for n in numbers[1:]:
        if n > result:
            result = n
    return result


# === 문제 6.1: 평균 점수 ===
def average_score(scores: list[float]) -> float:
    if not scores:
        return 0
    return sum(scores) / len(scores)


# === 문제 6.2: 두 리스트 합치기 ===
def merge_unique(a: list, b: list) -> list:
    return sorted(set(a) | set(b))


# === 문제 6.3: 단어 빈도 ===
def count_words(text: str) -> dict[str, int]:
    freq = {}
    for word in text.lower().split():
        freq[word] = freq.get(word, 0) + 1
    return freq


# === 문제 6.5: 가장 빈도 높은 요소 ===
def most_common(items: list) -> Any:
    from collections import Counter
    return Counter(items).most_common(1)[0][0]


# === 문제 7.1: 단어 뒤집기 ===
def reverse_words(s: str) -> str:
    return " ".join(s.split()[::-1])


# === 문제 7.2: 모음 개수 ===
def count_vowels(s: str) -> int:
    return sum(1 for c in s.lower() if c in "aeiou")


# === 문제 7.3: 압축 ===
def compress(s: str) -> str:
    if not s:
        return ""

    result = []
    current = s[0]
    count = 1

    for char in s[1:]:
        if char == current:
            count += 1
        else:
            result.append(f"{current}{count}")
            current = char
            count = 1

    result.append(f"{current}{count}")
    return "".join(result)


# === 문제 7.4: 비밀번호 강도 ===
def is_strong_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True


# === 문제 7.5: 문장 첫 글자 대문자 ===
def capitalize_sentences(text: str) -> str:
    sentences = text.split(". ")
    capitalized = [s[0].upper() + s[1:] if s else s for s in sentences]
    return ". ".join(capitalized)


# === 검증 ===
if __name__ == "__main__":
    # 테스트
    assert sum_between(1, 5) == 15
    assert sum_between(5, 1) == 15  # 순서 상관없이
    assert factorial(5) == 120
    assert factorial(0) == 1
    assert is_palindrome("level") == True
    assert is_palindrome("hello") == False
    assert is_palindrome("A man a plan") == False  # 'amanplan' != reverse
    assert average(1, 2, 3, 4, 5) == 3.0
    assert my_max(3, 1, 4, 1, 5, 9, 2, 6) == 9
    assert count_words("the the the cat") == {"the": 3, "cat": 1}
    assert most_common([1, 2, 2, 3, 2]) == 2
    assert reverse_words("Hello World Python") == "Python World Hello"
    assert count_vowels("Hello World") == 3
    assert compress("aaabbbccd") == "a3b3c2d1"
    assert is_strong_password("Pass1234") == True
    assert is_strong_password("password") == False
    assert capitalize_sentences("hello. world").startswith("Hello")

    print("✅ 모든 테스트 통과!")

    # 시연
    print("\n=== Primes up to 30 ===")
    print(primes_up_to(30))

    print("\n=== Pyramid (n=5) ===")
    pyramid(5)
