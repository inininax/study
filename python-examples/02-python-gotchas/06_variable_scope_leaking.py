"""
06_variable_scope_leaking.py - 🟡 변수 스코프 누출

📌 핵심 개념:
    Python에는 블록 스코프가 없습니다!
    for 문, if 문, with 문 안에서 정의한 변수가 바깥에서도 접근 가능합니다.

🔄 다른 언어 비교:
    - Java: 블록 스코프 있음 ({}로 제한)
    - Go: 블록 스코프 있음
    - Kotlin: 블록 스코프 있음
    - Python: 블록 스코프 없음! (함수 스코프만)

⚠️ 주의사항:
    - for 루프 변수가 바깥에서 사용 가능
    - 변수명 충돌에 주의
    - comprehension은 예외 (Python 3+에서 자체 스코프)

📚 참고: https://docs.python.org/3/reference/executionmodel.html#naming-and-binding
"""

from __future__ import annotations


# =============================================================================
# 1️⃣ for 문 변수 누출
# =============================================================================

def for_loop_leaking_demo() -> None:
    """
    for 문 변수 누출 시연.
    
    💡 Java 개발자를 위한 팁:
        Java에서 for 문 변수는 블록 내부에서만 접근 가능합니다.
        
        Java:
            for (int i = 0; i < 5; i++) { ... }
            System.out.println(i);  // 컴파일 에러!
            
        Python:
            for i in range(5): ...
            print(i)  # 4 출력! 에러 없음!
    """
    print("for 문 변수 누출:")
    
    for i in range(5):
        x = i * 2
    
    # 루프 변수와 내부 변수 모두 접근 가능!
    print(f"  루프 종료 후 i = {i}")  # 4
    print(f"  루프 내부 x = {x}")      # 8
    
    # 흔한 실수: 변수명 재사용
    items = ["a", "b", "c"]
    
    for item in items:
        pass
    
    # 이후 코드에서 item 사용 (의도치 않게)
    print(f"  루프 후 item = '{item}'")  # 'c'


# =============================================================================
# 2️⃣ if 문 변수 누출
# =============================================================================

def if_statement_leaking_demo() -> None:
    """
    if 문 변수 누출 시연.
    """
    print("if 문 변수 누출:")
    
    condition = True
    
    if condition:
        value = "true branch"
    else:
        value = "false branch"
    
    # if 블록 바깥에서도 접근 가능
    print(f"  if 블록 밖에서 value = '{value}'")
    
    # ⚠️ 주의: 조건에 따라 변수가 없을 수 있음
    condition = False
    
    if condition:
        another_value = "defined"
    
    # 조건이 거짓이면 another_value가 정의되지 않음!
    try:
        print(another_value)  # type: ignore
    except NameError as e:
        print(f"  ⚠️ NameError: {e}")


# =============================================================================
# 3️⃣ with 문 변수 누출
# =============================================================================

def with_statement_leaking_demo() -> None:
    """
    with 문 변수 누출 시연.
    """
    import tempfile
    import os
    
    print("with 문 변수 누출:")
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test")
        filepath = f.name
    
    # with 블록 종료 후에도 f 접근 가능!
    print(f"  with 블록 밖에서 f = {f}")
    print(f"  f.closed = {f.closed}")  # True (닫혔지만 변수는 존재)
    
    os.unlink(filepath)
    
    # 일반적인 패턴
    with open(__file__) as file:
        first_line = file.readline()
    
    # file 변수는 존재하지만 닫힘
    print(f"  file.closed = {file.closed}")


# =============================================================================
# 4️⃣ Comprehension의 스코프 (예외)
# =============================================================================

def comprehension_scope_demo() -> None:
    """
    Comprehension은 자체 스코프가 있습니다 (Python 3+).
    
    ⚠️ Python 2에서는 comprehension도 누출되었습니다!
    """
    print("Comprehension 스코프 (Python 3+):")
    
    # List Comprehension
    squares = [x**2 for x in range(5)]
    print(f"  squares = {squares}")
    
    try:
        print(f"  x = {x}")  # type: ignore  # NameError!
    except NameError:
        print("  ✅ x는 comprehension 내부에서만 존재 (Python 3+)")
    
    # 대조: for 문
    squares_for = []
    for y in range(5):
        squares_for.append(y**2)
    
    print(f"  squares_for = {squares_for}")
    print(f"  for 문의 y = {y}")  # 4 - 누출됨!
    
    # Generator Expression도 마찬가지
    gen = (z**2 for z in range(5))
    try:
        print(f"  z = {z}")  # type: ignore
    except NameError:
        print("  ✅ z도 generator 내부에서만 존재")


# =============================================================================
# 5️⃣ 함수 스코프
# =============================================================================

def function_scope_demo() -> None:
    """
    Python은 함수 스코프를 가집니다.
    """
    print("함수 스코프:")
    
    def outer() -> None:
        outer_var = "outer"
        
        def inner() -> None:
            inner_var = "inner"
            print(f"    inner에서 outer_var: {outer_var}")
            print(f"    inner에서 inner_var: {inner_var}")
        
        inner()
        print(f"    outer에서 outer_var: {outer_var}")
        try:
            print(inner_var)  # type: ignore
        except NameError:
            print("    ✅ inner_var는 inner 함수 내부에서만 존재")
    
    outer()
    
    try:
        print(outer_var)  # type: ignore
    except NameError:
        print("  ✅ outer_var는 outer 함수 내부에서만 존재")


# =============================================================================
# 6️⃣ 실수하기 쉬운 패턴
# =============================================================================

def common_mistakes_demo() -> None:
    """
    변수 스코프 관련 실수.
    """
    print("실수하기 쉬운 패턴:")
    
    # 1. 루프 변수 재사용
    print("\n  1. 루프 변수 재사용:")
    
    users = [{"name": "Kim"}, {"name": "Lee"}]
    
    for user in users:
        print(f"    Processing: {user['name']}")
    
    # 나중에 다른 목적으로 user 사용 (실수)
    admin = user  # 마지막 user를 참조!
    print(f"    admin (실수로 마지막 user 참조): {admin}")
    
    # 2. 조건부 변수 정의
    print("\n  2. 조건부 변수 정의:")
    
    def process(data: list[int]) -> str:
        if data:
            result = sum(data)
        # else 브랜치에서 result 정의 안 함!
        
        # data가 비어있으면 result가 정의되지 않음
        try:
            return f"Sum: {result}"
        except UnboundLocalError:
            return "No data"
    
    print(f"    process([1, 2, 3]): {process([1, 2, 3])}")
    print(f"    process([]): {process([])}")
    
    # ✅ 올바른 패턴: 미리 초기화
    def process_correct(data: list[int]) -> str:
        result = 0  # 기본값 초기화
        if data:
            result = sum(data)
        return f"Sum: {result}"
    
    print(f"    process_correct([]): {process_correct([])}")


# =============================================================================
# 7️⃣ 요약
# =============================================================================

def summary() -> None:
    """
    변수 스코프 요약.
    """
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                  🟡 Python 스코프 규칙                         ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║  Python에는 블록 스코프가 없습니다!                           ║
    ║                                                               ║
    ║  스코프 종류:                                                 ║
    ║    - 함수 스코프 (function scope) ✅                          ║
    ║    - 클래스 스코프                                            ║
    ║    - 모듈 스코프 (global)                                     ║
    ║    - 블록 스코프 ❌ (없음!)                                    ║
    ║                                                               ║
    ║  누출되는 변수:                                               ║
    ║    - for 루프 변수                                            ║
    ║    - if/else 내부 변수                                        ║
    ║    - with 문의 as 변수                                        ║
    ║    - try/except의 변수                                        ║
    ║                                                               ║
    ║  예외 (자체 스코프):                                          ║
    ║    - List/Dict/Set Comprehension (Python 3+)                  ║
    ║    - Generator Expression                                     ║
    ║    - 함수 (def, lambda)                                       ║
    ║                                                               ║
    ║  💡 권장 사항:                                                 ║
    ║    - 변수명을 명확하게 짓기                                   ║
    ║    - 필요한 변수는 미리 초기화                                ║
    ║    - 루프 변수 재사용 피하기                                  ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)


# =============================================================================
# 메인 실행
# =============================================================================

def main() -> None:
    """예제 실행."""
    demos = [
        ("1️⃣ for 문 누출", for_loop_leaking_demo),
        ("2️⃣ if 문 누출", if_statement_leaking_demo),
        ("3️⃣ with 문 누출", with_statement_leaking_demo),
        ("4️⃣ Comprehension 스코프", comprehension_scope_demo),
        ("5️⃣ 함수 스코프", function_scope_demo),
        ("6️⃣ 실수 패턴", common_mistakes_demo),
        ("7️⃣ 요약", summary),
    ]
    
    print("=" * 60)
    print("🟡 변수 스코프 누출")
    print("=" * 60)
    print()
    
    for title, demo_func in demos:
        print("-" * 60)
        print(f"📌 {title}")
        print("-" * 60)
        demo_func()
        print()


if __name__ == "__main__":
    main()

