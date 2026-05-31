"""
01. Python 소개 — Hello World

가장 기본적인 Python 프로그램.
참고: ../../01-beginner/01-introduction.md
"""

# 기본 출력
print("Hello, World!")
print("안녕하세요, Python!")

# 여러 줄
print("첫 번째 줄")
print("두 번째 줄")

# 한 줄에 여러 값
print("a", "b", "c")              # a b c
print("a", "b", "c", sep="-")      # a-b-c
print("Hello", end=" ")
print("World")                     # Hello World

# 변수와 함께
name = "Python"
version = 3.12
print(f"Welcome to {name} {version}!")

# 사용자 입력 (주석 처리 - 자동 실행을 위해)
# user_name = input("이름을 입력하세요: ")
# print(f"안녕하세요, {user_name}님!")
