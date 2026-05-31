"""
01_syntax_comparison.py - Java/Go 스타일 vs Python 스타일 비교

📌 핵심 개념:
    다른 언어 개발자가 Python으로 전환할 때 문법적 차이를 빠르게 이해

🔄 다른 언어 비교:
    - Java: 명시적 타입, 세미콜론, 중괄호 블록
    - Go: 짧은 변수 선언(:=), 명시적 에러 처리
    - Kotlin: 간결한 문법, data class
    - Python: 동적 타이핑, 들여쓰기 블록, 간결함

⚠️ 주의사항:
    Python에서는 들여쓰기가 문법입니다. 탭과 스페이스를 섞지 마세요!

📚 참고: https://docs.python.org/3/tutorial/
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


# =============================================================================
# 1️⃣ 변수 선언 비교
# =============================================================================

def variable_declaration_demo() -> None:
    """
    변수 선언 방식 비교.
    
    💡 Java/Go 개발자를 위한 팁:
        - Java: `int age = 30;` - 타입 먼저, 세미콜론 필수
        - Go: `age := 30` 또는 `var age int = 30`
        - Python: `age = 30` 또는 `age: int = 30` (타입 힌트)
        
        Python의 타입 힌트는 런타임에 강제되지 않습니다!
        mypy 같은 도구로 정적 분석 시에만 검사됩니다.
    """
    # Python 스타일 - 타입 힌트 없이
    name = "Kim"
    age = 30
    is_active = True
    
    # Python 스타일 - 타입 힌트 포함 (권장)
    name_typed: str = "Kim"
    age_typed: int = 30
    is_active_typed: bool = True
    
    # 여러 변수 동시 할당 (Python만의 기능)
    x, y, z = 1, 2, 3
    
    # 값 교환 (Java/Go에서는 임시 변수 필요)
    a, b = 10, 20
    a, b = b, a  # 파이썬은 이렇게 간단!
    
    print(f"name: {name_typed}, age: {age_typed}")
    print(f"좌표: ({x}, {y}, {z})")
    print(f"교환 후: a={a}, b={b}")


# =============================================================================
# 2️⃣ 컬렉션 비교
# =============================================================================

def collections_demo() -> None:
    """
    컬렉션 사용법 비교.
    
    💡 Java 개발자를 위한 팁:
        - ArrayList → list
        - HashMap → dict
        - HashSet → set
        
        Python 컬렉션은 기본적으로 가변(mutable)입니다.
        불변이 필요하면 tuple, frozenset을 사용하세요.
    """
    # List (Java의 ArrayList, Go의 slice)
    numbers: list[int] = [1, 2, 3, 4, 5]
    numbers.append(6)  # Java: list.add(6)
    numbers.extend([7, 8])  # Java: list.addAll(Arrays.asList(7, 8))
    
    # Dict (Java의 HashMap, Go의 map)
    person: dict[str, str | int] = {
        "name": "Kim",
        "age": 30,
        "city": "Seoul"
    }
    person["email"] = "kim@example.com"  # Java: map.put("email", "...")
    
    # Set (Java의 HashSet)
    unique_numbers: set[int] = {1, 2, 3, 3, 3}  # {1, 2, 3}
    unique_numbers.add(4)
    
    # Tuple (불변 리스트) - Java에는 없음, Kotlin의 Pair/Triple 유사
    point: tuple[int, int] = (10, 20)
    # point[0] = 100  # 에러! tuple은 불변
    
    print(f"List: {numbers}")
    print(f"Dict: {person}")
    print(f"Set: {unique_numbers}")
    print(f"Tuple: {point}")


# =============================================================================
# 3️⃣ 조건문 비교
# =============================================================================

def conditionals_demo() -> None:
    """
    조건문 비교.
    
    💡 Java/Go 개발자를 위한 팁:
        - 중괄호 {} 대신 콜론(:)과 들여쓰기 사용
        - else if → elif
        - switch문 없음 → match문 (Python 3.10+) 또는 dict 매핑
    """
    score = 85
    
    # if-elif-else (Java의 if-else if-else)
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    else:
        grade = "F"
    
    print(f"점수: {score}, 학점: {grade}")
    
    # 삼항 연산자 (Java: condition ? a : b)
    status = "합격" if score >= 60 else "불합격"
    print(f"상태: {status}")
    
    # match문 (Python 3.10+) - Java의 switch 유사
    http_status = 200
    match http_status:
        case 200:
            message = "OK"
        case 404:
            message = "Not Found"
        case 500:
            message = "Server Error"
        case _:  # default
            message = "Unknown"
    
    print(f"HTTP {http_status}: {message}")


# =============================================================================
# 4️⃣ 반복문 비교
# =============================================================================

def loops_demo() -> None:
    """
    반복문 비교.
    
    💡 Java/Go 개발자를 위한 팁:
        - for (int i = 0; i < n; i++) → for i in range(n)
        - for-each → for item in collection
        - while문은 동일
        - do-while 없음!
    """
    # range를 이용한 반복 (Java의 전통적 for문)
    print("range 반복:")
    for i in range(5):  # 0, 1, 2, 3, 4
        print(f"  i = {i}")
    
    # 컬렉션 순회 (Java의 for-each)
    fruits = ["apple", "banana", "cherry"]
    print("\n컬렉션 순회:")
    for fruit in fruits:
        print(f"  {fruit}")
    
    # enumerate - 인덱스와 값 동시에 (Java에서는 별도 카운터 필요)
    print("\nenumerate 사용:")
    for idx, fruit in enumerate(fruits):
        print(f"  [{idx}] {fruit}")
    
    # dict 순회
    person = {"name": "Kim", "age": 30}
    print("\ndict 순회:")
    for key, value in person.items():
        print(f"  {key}: {value}")
    
    # List Comprehension (Java에 없는 기능!)
    squares = [x**2 for x in range(10)]
    print(f"\nList Comprehension: {squares}")
    
    # 조건부 List Comprehension
    even_squares = [x**2 for x in range(10) if x % 2 == 0]
    print(f"짝수만: {even_squares}")


# =============================================================================
# 5️⃣ 함수 비교
# =============================================================================

def functions_demo() -> None:
    """
    함수 정의 비교.
    
    💡 Java/Go 개발자를 위한 팁:
        - 반환 타입은 -> 뒤에 (Java: 메서드명 앞)
        - 기본값 인자 지원 (Java는 오버로딩 필요)
        - *args, **kwargs로 가변 인자 처리
    """
    
    # 기본 함수
    def add(a: int, b: int) -> int:
        """두 수를 더합니다."""
        return a + b
    
    # 기본값 인자 (Java에서는 오버로딩 필요)
    def greet(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}!"
    
    # 여러 값 반환 (Java에서는 객체나 Pair 필요)
    def get_user_info() -> tuple[str, int, str]:
        return "Kim", 30, "Seoul"
    
    # 가변 인자 (*args)
    def sum_all(*numbers: int) -> int:
        return sum(numbers)
    
    # 키워드 가변 인자 (**kwargs)
    def print_info(**info: str) -> None:
        for key, value in info.items():
            print(f"  {key}: {value}")
    
    print(f"add(3, 5) = {add(3, 5)}")
    print(f"greet('Kim') = {greet('Kim')}")
    print(f"greet('Kim', 'Hi') = {greet('Kim', 'Hi')}")
    
    name, age, city = get_user_info()  # Unpacking
    print(f"User: {name}, {age}, {city}")
    
    print(f"sum_all(1, 2, 3, 4, 5) = {sum_all(1, 2, 3, 4, 5)}")
    
    print("print_info:")
    print_info(name="Kim", role="Developer", team="Backend")


# =============================================================================
# 6️⃣ 클래스 비교
# =============================================================================

def classes_demo() -> None:
    """
    클래스 정의 비교.
    
    💡 Java/Kotlin 개발자를 위한 팁:
        - __init__이 생성자 (Java의 constructor)
        - self가 명시적 (Java의 this는 암시적)
        - @dataclass는 Kotlin의 data class와 유사
        - private은 관례적으로 _prefix 사용 (강제 아님)
    """
    
    # 전통적인 클래스
    class Person:
        """전통적인 Python 클래스."""
        
        def __init__(self, name: str, age: int) -> None:
            self.name = name  # public (관례)
            self.age = age
            self._email: str | None = None  # protected (관례)
        
        def greet(self) -> str:
            return f"Hello, I'm {self.name}"
        
        def __str__(self) -> str:
            return f"Person(name={self.name}, age={self.age})"
    
    # dataclass (Kotlin의 data class, Java 14+ record)
    @dataclass
    class User:
        """dataclass - 보일러플레이트 감소."""
        name: str
        age: int
        email: str = ""  # 기본값
        
        def is_adult(self) -> bool:
            return self.age >= 18
    
    person = Person("Kim", 30)
    print(f"Person: {person}")
    print(f"Greet: {person.greet()}")
    
    user = User("Lee", 25, "lee@example.com")
    print(f"User: {user}")
    print(f"Is adult: {user.is_adult()}")


# =============================================================================
# 7️⃣ 예외 처리 비교
# =============================================================================

def exception_handling_demo() -> None:
    """
    예외 처리 비교.
    
    💡 Java/Go 개발자를 위한 팁:
        - Java: try-catch-finally
        - Go: if err != nil (명시적 에러 반환)
        - Python: try-except-finally (else 블록도 있음!)
        
        Go 개발자: Python에서도 Optional 반환 패턴 사용 가능하지만,
        예외 처리가 더 Pythonic합니다.
    """
    
    def divide(a: int, b: int) -> float:
        """나눗셈 (예외 발생 가능)."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    # try-except-else-finally
    try:
        result = divide(10, 2)
    except ValueError as e:
        print(f"에러 발생: {e}")
    else:
        # 예외가 발생하지 않았을 때만 실행
        print(f"결과: {result}")
    finally:
        # 항상 실행
        print("정리 작업 완료")
    
    # 여러 예외 처리
    def safe_operation(data: str) -> Optional[int]:
        try:
            return int(data)
        except (ValueError, TypeError):
            return None
    
    print(f"safe_operation('123') = {safe_operation('123')}")
    print(f"safe_operation('abc') = {safe_operation('abc')}")


# =============================================================================
# 메인 실행
# =============================================================================

def main() -> None:
    """예제 실행."""
    demos = [
        ("1️⃣ 변수 선언", variable_declaration_demo),
        ("2️⃣ 컬렉션", collections_demo),
        ("3️⃣ 조건문", conditionals_demo),
        ("4️⃣ 반복문", loops_demo),
        ("5️⃣ 함수", functions_demo),
        ("6️⃣ 클래스", classes_demo),
        ("7️⃣ 예외 처리", exception_handling_demo),
    ]
    
    for title, demo_func in demos:
        print("=" * 60)
        print(f"📌 {title}")
        print("=" * 60)
        demo_func()
        print()


if __name__ == "__main__":
    main()

