"""
01_variables_and_types.py - 동적 타이핑 vs 정적 타이핑

📌 핵심 개념:
    Python은 동적 타이핑 언어입니다. 변수에 타입이 없고, 값에 타입이 있습니다.
    하지만 타입 힌트를 통해 정적 분석이 가능합니다.

🔄 다른 언어 비교:
    - Java: 정적 타이핑, 변수 선언 시 타입 필수
    - Go: 정적 타이핑, 타입 추론 가능하지만 변경 불가
    - Kotlin: 정적 타이핑, val/var로 불변/가변 구분
    - Python: 동적 타이핑, 런타임에 타입 결정

⚠️ 주의사항:
    타입 힌트는 런타임에 강제되지 않습니다!
    mypy 같은 정적 분석 도구를 사용해야 타입 검사가 됩니다.

📚 참고: https://docs.python.org/3/library/typing.html
"""

from __future__ import annotations

from typing import Any, Final, Union


# =============================================================================
# 1️⃣ 동적 타이핑 이해
# =============================================================================

def dynamic_typing_demo() -> None:
    """
    동적 타이핑 - 변수가 아닌 값에 타입이 있다.
    
    💡 Java 개발자를 위한 팁:
        Java에서는 불가능한 코드입니다:
        ```java
        int x = 10;
        x = "hello";  // 컴파일 에러!
        ```
        
        Python에서는 변수는 단지 "이름표"일 뿐입니다.
    """
    x = 10
    print(f"x = {x}, type = {type(x)}")  # <class 'int'>
    
    x = "hello"  # 같은 변수에 다른 타입 할당 가능!
    print(f"x = {x}, type = {type(x)}")  # <class 'str'>
    
    x = [1, 2, 3]
    print(f"x = {x}, type = {type(x)}")  # <class 'list'>
    
    # 하지만 연산은 타입에 따라 다르게 동작
    print("\n타입에 따른 + 연산:")
    print(f"10 + 20 = {10 + 20}")  # 정수 덧셈
    print(f"'hello' + ' world' = {'hello' + ' world'}")  # 문자열 연결
    print(f"[1, 2] + [3, 4] = {[1, 2] + [3, 4]}")  # 리스트 연결


# =============================================================================
# 2️⃣ 타입 힌트 (Type Hints)
# =============================================================================

def type_hints_demo() -> None:
    """
    타입 힌트 - 정적 분석을 위한 타입 어노테이션.
    
    💡 Java 개발자를 위한 팁:
        Java의 타입 선언과 비슷하게 생겼지만, 런타임에 강제되지 않습니다!
        단지 IDE 자동완성과 mypy 같은 도구를 위한 것입니다.
    """
    # 변수에 타입 힌트
    name: str = "Kim"
    age: int = 30
    scores: list[float] = [85.5, 90.0, 78.5]
    
    # 타입 힌트가 있어도 다른 타입 할당 가능 (런타임 에러 없음!)
    # age = "thirty"  # mypy는 에러 표시, 하지만 실행은 됨
    
    print(f"name: {name} ({type(name).__name__})")
    print(f"age: {age} ({type(age).__name__})")
    print(f"scores: {scores}")
    
    # 복잡한 타입
    user: dict[str, str | int] = {
        "name": "Kim",
        "age": 30,
    }
    print(f"user: {user}")


# =============================================================================
# 3️⃣ 상수와 Final
# =============================================================================

def constants_demo() -> None:
    """
    상수 - Python에는 진짜 상수가 없다!
    
    💡 Java 개발자를 위한 팁:
        Java의 final이나 Go의 const와 달리, Python의 Final은 관례입니다.
        런타임에 재할당을 막지 않습니다.
        
    💡 Kotlin 개발자를 위한 팁:
        Kotlin의 val도 불변이지만 컴파일러가 강제합니다.
        Python의 Final은 mypy가 검사할 뿐입니다.
    """
    # 관례: 대문자 = 상수
    MAX_CONNECTIONS = 100
    API_BASE_URL = "https://api.example.com"
    
    # Final 타입 힌트 (Python 3.8+)
    DATABASE_URL: Final = "postgresql://localhost/db"
    
    print(f"MAX_CONNECTIONS: {MAX_CONNECTIONS}")
    print(f"API_BASE_URL: {API_BASE_URL}")
    print(f"DATABASE_URL: {DATABASE_URL}")
    
    # ⚠️ 하지만 재할당 가능! (권장하지 않음)
    # MAX_CONNECTIONS = 200  # mypy 에러, 하지만 실행은 됨


# =============================================================================
# 4️⃣ 타입 검사 방법
# =============================================================================

def type_checking_demo() -> None:
    """
    런타임 타입 검사 방법.
    
    💡 Java 개발자를 위한 팁:
        instanceof 대신 isinstance()를 사용합니다.
        하지만 Python에서는 EAFP(허락보다 용서)가 더 권장됩니다.
    """
    value: Any = "hello"
    
    # isinstance() - 타입 검사
    if isinstance(value, str):
        print(f"'{value}'는 문자열입니다")
    
    # 여러 타입 검사
    def process(data: int | str | list[Any]) -> str:
        if isinstance(data, int):
            return f"정수: {data}"
        elif isinstance(data, str):
            return f"문자열: {data}"
        elif isinstance(data, list):
            return f"리스트: {data}"
        return "알 수 없는 타입"
    
    print(process(42))
    print(process("hello"))
    print(process([1, 2, 3]))
    
    # type() vs isinstance()
    print("\ntype() vs isinstance():")
    
    class Animal:
        pass
    
    class Dog(Animal):
        pass
    
    dog = Dog()
    print(f"type(dog) == Dog: {type(dog) == Dog}")  # True
    print(f"type(dog) == Animal: {type(dog) == Animal}")  # False!
    print(f"isinstance(dog, Dog): {isinstance(dog, Dog)}")  # True
    print(f"isinstance(dog, Animal): {isinstance(dog, Animal)}")  # True (상속 고려)


# =============================================================================
# 5️⃣ 덕 타이핑 (Duck Typing)
# =============================================================================

def duck_typing_demo() -> None:
    """
    덕 타이핑 - "오리처럼 걷고 오리처럼 꽥꽥거리면, 그것은 오리다"
    
    💡 Java 개발자를 위한 팁:
        Java에서는 interface를 구현해야 같은 타입으로 취급됩니다.
        Python에서는 같은 메서드만 있으면 됩니다!
        
    💡 Go 개발자를 위한 팁:
        Go의 implicit interface 구현과 매우 유사합니다.
    """
    
    class Duck:
        def quack(self) -> str:
            return "꽥꽥!"
        
        def walk(self) -> str:
            return "뒤뚱뒤뚱"
    
    class Person:
        def quack(self) -> str:
            return "사람이 꽥꽥 흉내"
        
        def walk(self) -> str:
            return "걷기"
    
    class Robot:
        def quack(self) -> str:
            return "삐빕 꽥"
        
        def walk(self) -> str:
            return "철컹철컹"
    
    # 타입에 관계없이 같은 인터페이스 사용
    def make_it_quack(duck_like: Any) -> None:
        # 인터페이스 구현 여부를 검사하지 않음
        # 그냥 quack() 메서드가 있으면 호출
        print(f"{type(duck_like).__name__}: {duck_like.quack()}")
    
    make_it_quack(Duck())
    make_it_quack(Person())
    make_it_quack(Robot())
    
    print("\n💡 덕 타이핑의 장단점:")
    print("  장점: 유연함, 빠른 개발")
    print("  단점: 런타임 에러 가능성, IDE 지원 약함")


# =============================================================================
# 6️⃣ EAFP vs LBYL
# =============================================================================

def eafp_vs_lbyl_demo() -> None:
    """
    EAFP (Easier to Ask Forgiveness than Permission) vs
    LBYL (Look Before You Leap)
    
    💡 Java/Go 개발자를 위한 팁:
        - LBYL은 Java/Go에서 익숙한 패턴 (조건 검사 후 실행)
        - EAFP는 Python이 권장하는 패턴 (일단 실행, 에러 시 처리)
        
        Python에서는 EAFP가 더 Pythonic합니다!
    """
    data: dict[str, Any] = {"name": "Kim", "age": 30}
    
    # LBYL (Java/Go 스타일) - 먼저 확인
    print("LBYL 스타일:")
    if "email" in data:
        email = data["email"]
    else:
        email = "없음"
    print(f"  email: {email}")
    
    # EAFP (Pythonic) - 일단 시도
    print("\nEAFP 스타일:")
    try:
        email = data["email"]
    except KeyError:
        email = "없음"
    print(f"  email: {email}")
    
    # 가장 Pythonic한 방법
    print("\n가장 Pythonic:")
    email = data.get("email", "없음")
    print(f"  email: {email}")
    
    # 파일 존재 확인 예시
    print("\n파일 처리 예시:")
    import os
    
    # LBYL
    filepath = "/tmp/test.txt"
    print(f"  LBYL: if os.path.exists('{filepath}'): ...")
    
    # EAFP (권장)
    print("  EAFP: try: open(...) except FileNotFoundError: ...")


# =============================================================================
# 메인 실행
# =============================================================================

def main() -> None:
    """예제 실행."""
    demos = [
        ("1️⃣ 동적 타이핑", dynamic_typing_demo),
        ("2️⃣ 타입 힌트", type_hints_demo),
        ("3️⃣ 상수와 Final", constants_demo),
        ("4️⃣ 타입 검사", type_checking_demo),
        ("5️⃣ 덕 타이핑", duck_typing_demo),
        ("6️⃣ EAFP vs LBYL", eafp_vs_lbyl_demo),
    ]
    
    for title, demo_func in demos:
        print("=" * 60)
        print(f"📌 {title}")
        print("=" * 60)
        demo_func()
        print()


if __name__ == "__main__":
    main()

