"""
05_unpacking_magic.py - *args, **kwargs, Unpacking 마스터

📌 핵심 개념:
    Python의 언패킹(Unpacking)은 컬렉션의 요소를 개별 변수로 분해합니다.
    *args와 **kwargs는 가변 인자를 처리하는 Python의 관례입니다.

🔄 다른 언어 비교:
    - Java: 배열 인덱스로 접근, varargs(...) 제한적
    - Go: 슬라이스로 vararg, 언패킹 없음
    - Kotlin: vararg, destructuring declaration
    - Python: *args, **kwargs, 유연한 언패킹

⚠️ 주의사항:
    - *는 iterable 언패킹 (리스트, 튜플)
    - **는 dict 언패킹
    - 언패킹 시 개수가 맞아야 합니다!

📚 참고: https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists
"""

from __future__ import annotations

from typing import Any


# =============================================================================
# 1️⃣ 기본 언패킹 (Unpacking)
# =============================================================================

def basic_unpacking_demo() -> None:
    """
    기본 언패킹 문법.
    
    💡 Java 개발자를 위한 팁:
        Java에는 언패킹이 없습니다!
        배열 요소를 개별 변수에 할당하려면 인덱스로 접근해야 합니다.
        
        Java:
            int[] arr = {1, 2, 3};
            int a = arr[0], b = arr[1], c = arr[2];
            
        Python:
            arr = (1, 2, 3)
            a, b, c = arr
            
    💡 Kotlin 개발자를 위한 팁:
        Kotlin의 destructuring declaration과 유사합니다.
        
        Kotlin: val (a, b, c) = listOf(1, 2, 3)
        Python: a, b, c = [1, 2, 3]
    """
    # 튜플 언패킹
    point = (10, 20, 30)
    x, y, z = point
    print(f"point = {point}")
    print(f"x={x}, y={y}, z={z}")
    
    # 리스트 언패킹
    colors = ["red", "green", "blue"]
    r, g, b = colors
    print(f"\ncolors = {colors}")
    print(f"r={r}, g={g}, b={b}")
    
    # 문자열 언패킹
    chars = "ABC"
    a, b, c = chars
    print(f"\nchars = '{chars}'")
    print(f"a='{a}', b='{b}', c='{c}'")
    
    # 값 교환 (swap) - 언패킹의 대표적 활용
    left, right = 1, 2
    print(f"\nBefore: left={left}, right={right}")
    left, right = right, left  # 임시 변수 없이 교환!
    print(f"After: left={left}, right={right}")
    
    # 언패킹 + 무시
    data = (1, 2, 3, 4, 5)
    first, second, *_ = data  # 나머지 무시
    print(f"\nfirst={first}, second={second}")
    
    a, *middle, z = data  # 처음과 끝만
    print(f"a={a}, middle={middle}, z={z}")


# =============================================================================
# 2️⃣ 확장 언패킹 (Extended Unpacking)
# =============================================================================

def extended_unpacking_demo() -> None:
    """
    * 연산자를 활용한 확장 언패킹.
    
    💡 핵심:
        *변수는 "나머지 모든 요소"를 리스트로 받습니다.
    """
    # *를 사용한 나머지 캡처
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    first, *rest = numbers
    print(f"first={first}, rest={rest}")
    
    *most, last = numbers
    print(f"most={most}, last={last}")
    
    head, *body, tail = numbers
    print(f"head={head}, body={body}, tail={tail}")
    
    # 중첩 언패킹
    nested = [[1, 2], [3, 4], [5, 6]]
    (a, b), (c, d), (e, f) = nested
    print(f"\n중첩 언패킹: a={a}, b={b}, c={c}, d={d}, e={e}, f={f}")
    
    # for문에서의 언패킹
    pairs = [("Alice", 30), ("Bob", 25), ("Charlie", 35)]
    print("\nfor문 언패킹:")
    for name, age in pairs:
        print(f"  {name}: {age}살")
    
    # enumerate와 함께
    print("\nenumerate + 언패킹:")
    for i, (name, age) in enumerate(pairs):
        print(f"  [{i}] {name}: {age}살")


# =============================================================================
# 3️⃣ *args - 위치 인자 가변
# =============================================================================

def args_demo() -> None:
    """
    *args - 가변 위치 인자.
    
    💡 Java 개발자를 위한 팁:
        Java의 varargs(...)와 유사하지만 더 유연합니다.
        
        Java: void method(String... args)
        Python: def method(*args)
        
        차이점:
        - Java varargs는 마지막에만 가능
        - Python *args는 다른 인자와 조합 가능
    """
    # 기본 *args
    def sum_all(*numbers: int) -> int:
        """모든 인자의 합계."""
        print(f"  numbers = {numbers}, type = {type(numbers)}")
        return sum(numbers)
    
    print("sum_all 호출:")
    print(f"  sum_all(1, 2, 3) = {sum_all(1, 2, 3)}")
    print(f"  sum_all(1, 2, 3, 4, 5) = {sum_all(1, 2, 3, 4, 5)}")
    print(f"  sum_all() = {sum_all()}")
    
    # 일반 인자 + *args
    def greet(greeting: str, *names: str) -> None:
        """인사말과 이름들."""
        for name in names:
            print(f"  {greeting}, {name}!")
    
    print("\ngreet 호출:")
    greet("Hello", "Alice", "Bob", "Charlie")
    
    # *args + keyword-only 인자
    def print_items(*items: str, sep: str = ", ", end: str = "\n") -> None:
        """아이템들을 구분자로 출력."""
        print(sep.join(items), end=end)
    
    print("\nprint_items 호출:")
    print_items("apple", "banana", "cherry")
    print_items("a", "b", "c", sep=" - ")
    
    # 리스트를 *로 언패킹해서 전달
    numbers_list = [1, 2, 3, 4, 5]
    print(f"\n리스트 언패킹: sum_all(*{numbers_list}) = {sum_all(*numbers_list)}")


# =============================================================================
# 4️⃣ **kwargs - 키워드 인자 가변
# =============================================================================

def kwargs_demo() -> None:
    """
    **kwargs - 가변 키워드 인자.
    
    💡 Java 개발자를 위한 팁:
        Java에는 이에 해당하는 기능이 없습니다!
        Map<String, Object>를 전달하는 것과 유사합니다.
    """
    # 기본 **kwargs
    def print_info(**info: Any) -> None:
        """키워드 인자들을 출력."""
        print(f"  kwargs = {info}, type = {type(info)}")
        for key, value in info.items():
            print(f"    {key}: {value}")
    
    print("print_info 호출:")
    print_info(name="Kim", age=30, city="Seoul")
    
    # 일반 인자 + **kwargs
    def create_user(name: str, **extras: Any) -> dict[str, Any]:
        """사용자 생성."""
        return {"name": name, **extras}
    
    print("\ncreate_user 호출:")
    user = create_user("Lee", age=25, role="admin", active=True)
    print(f"  {user}")
    
    # dict를 **로 언패킹해서 전달
    config = {"host": "localhost", "port": 8080, "debug": True}
    
    def connect(host: str, port: int, debug: bool = False) -> str:
        return f"Connected to {host}:{port} (debug={debug})"
    
    print(f"\ndict 언패킹: {connect(**config)}")
    
    # 기존 dict 병합 (Python 3.9+)
    defaults = {"theme": "dark", "lang": "ko"}
    user_prefs = {"theme": "light"}
    merged = {**defaults, **user_prefs}
    print(f"\ndict 병합: {merged}")


# =============================================================================
# 5️⃣ *args와 **kwargs 조합
# =============================================================================

def args_kwargs_combined_demo() -> None:
    """
    *args와 **kwargs를 함께 사용.
    
    💡 인자 순서 규칙:
        1. 일반 위치 인자
        2. *args
        3. keyword-only 인자
        4. **kwargs
    """
    # 모든 인자 타입 조합
    def universal_function(
        required: str,           # 1. 필수 위치 인자
        optional: str = "opt",   # 2. 선택 위치 인자
        *args: Any,              # 3. 가변 위치 인자
        kwonly: str = "kw",      # 4. keyword-only 인자
        **kwargs: Any            # 5. 가변 키워드 인자
    ) -> None:
        """모든 인자 타입을 보여주는 함수."""
        print(f"  required = {required!r}")
        print(f"  optional = {optional!r}")
        print(f"  args = {args}")
        print(f"  kwonly = {kwonly!r}")
        print(f"  kwargs = {kwargs}")
    
    print("universal_function 호출:")
    print("\n1. 기본 호출:")
    universal_function("A")
    
    print("\n2. 모든 인자 사용:")
    universal_function("A", "B", "C", "D", kwonly="KW", extra1=1, extra2=2)
    
    # 래퍼 함수 패턴 (매우 흔함!)
    def wrapper_example(func):
        """함수를 감싸는 래퍼 예시."""
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f"  Calling {func.__name__}")
            print(f"    args: {args}")
            print(f"    kwargs: {kwargs}")
            return func(*args, **kwargs)
        return wrapper
    
    @wrapper_example
    def add(a: int, b: int) -> int:
        return a + b
    
    print("\n래퍼 패턴:")
    result = add(3, b=5)
    print(f"  result = {result}")


# =============================================================================
# 6️⃣ 실무 패턴
# =============================================================================

def practical_patterns_demo() -> None:
    """
    실무에서 자주 사용하는 언패킹 패턴.
    """
    # 1. 설정 오버라이드
    def get_config(**overrides: Any) -> dict[str, Any]:
        defaults = {
            "host": "localhost",
            "port": 8080,
            "debug": False,
            "timeout": 30,
        }
        return {**defaults, **overrides}
    
    config = get_config(port=3000, debug=True)
    print(f"설정 오버라이드: {config}")
    
    # 2. 함수 인자 전달 (프록시)
    def log_and_call(func, *args: Any, **kwargs: Any) -> Any:
        """함수 호출을 로깅."""
        print(f"  Calling: {func.__name__}({args}, {kwargs})")
        return func(*args, **kwargs)
    
    def greet(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}!"
    
    print(f"\n프록시 호출: {log_and_call(greet, 'Kim', greeting='Hi')}")
    
    # 3. 병렬 순회 (zip)
    names = ["Alice", "Bob", "Charlie"]
    ages = [30, 25, 35]
    cities = ["Seoul", "Busan", "Daegu"]
    
    print("\nzip 언패킹:")
    for name, age, city in zip(names, ages, cities):
        print(f"  {name}({age}) - {city}")
    
    # 4. dict를 키워드 인자로 (API 호출 등)
    def make_api_request(
        endpoint: str,
        method: str = "GET",
        headers: dict[str, str] | None = None,
        **params: Any
    ) -> str:
        return f"{method} {endpoint} headers={headers} params={params}"
    
    request_config = {
        "endpoint": "/users",
        "method": "POST",
        "headers": {"Authorization": "Bearer token"},
        "name": "Kim",
        "age": 30,
    }
    print(f"\nAPI 요청: {make_api_request(**request_config)}")
    
    # 5. 가변 생성자 (Django 모델 스타일)
    class User:
        def __init__(self, name: str, **attributes: Any) -> None:
            self.name = name
            for key, value in attributes.items():
                setattr(self, key, value)
        
        def __repr__(self) -> str:
            attrs = vars(self)
            return f"User({attrs})"
    
    user = User("Kim", age=30, role="admin", active=True)
    print(f"\n동적 속성: {user}")


# =============================================================================
# 메인 실행
# =============================================================================

def main() -> None:
    """예제 실행."""
    demos = [
        ("1️⃣ 기본 언패킹", basic_unpacking_demo),
        ("2️⃣ 확장 언패킹", extended_unpacking_demo),
        ("3️⃣ *args", args_demo),
        ("4️⃣ **kwargs", kwargs_demo),
        ("5️⃣ *args + **kwargs 조합", args_kwargs_combined_demo),
        ("6️⃣ 실무 패턴", practical_patterns_demo),
    ]
    
    for title, demo_func in demos:
        print("=" * 60)
        print(f"📌 {title}")
        print("=" * 60)
        demo_func()
        print()


if __name__ == "__main__":
    main()

