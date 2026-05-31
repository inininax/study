"""
03_functions_as_objects.py - 일급 함수 (First-Class Functions)

📌 핵심 개념:
    Python에서 함수는 "일급 객체(First-Class Object)"입니다.
    변수에 할당하고, 인자로 전달하고, 반환값으로 사용할 수 있습니다.

🔄 다른 언어 비교:
    - Java: 메서드는 일급 객체가 아님, 함수형 인터페이스로 우회
    - Go: 함수는 일급 객체 (func 타입)
    - Kotlin: 함수는 일급 객체 (람다, 고차 함수)
    - Python: 함수는 일급 객체

⚠️ 주의사항:
    함수를 변수에 할당할 때 ()를 붙이지 않습니다!
    func()는 함수 "호출", func는 함수 "참조"입니다.

📚 참고: https://docs.python.org/3/reference/datamodel.html
"""

from __future__ import annotations

from functools import partial, reduce
from typing import Callable, Any


# =============================================================================
# 1️⃣ 함수는 객체다
# =============================================================================

def function_as_object_demo() -> None:
    """
    함수도 객체입니다.
    
    💡 Java 개발자를 위한 팁:
        Java에서는 메서드를 변수에 직접 할당할 수 없습니다.
        Method Reference(::)나 함수형 인터페이스를 사용해야 합니다.
        
        Java:
            Function<Integer, Integer> square = x -> x * x;
            
        Python:
            def square(x): return x * x
            f = square  # 바로 할당 가능!
    """
    def greet(name: str) -> str:
        """인사 함수."""
        return f"Hello, {name}!"
    
    # 함수는 객체이므로 속성이 있다
    print(f"함수 이름: {greet.__name__}")
    print(f"함수 문서: {greet.__doc__}")
    print(f"함수 타입: {type(greet)}")
    
    # 변수에 할당
    say_hello = greet  # ()가 없으면 함수 참조!
    print(f"\nsay_hello('Python'): {say_hello('Python')}")
    
    # 리스트에 함수 저장
    def add(a: int, b: int) -> int:
        return a + b
    
    def subtract(a: int, b: int) -> int:
        return a - b
    
    def multiply(a: int, b: int) -> int:
        return a * b
    
    operations: list[Callable[[int, int], int]] = [add, subtract, multiply]
    
    print("\n함수 리스트 실행:")
    for op in operations:
        print(f"  {op.__name__}(10, 3) = {op(10, 3)}")


# =============================================================================
# 2️⃣ 고차 함수 (Higher-Order Functions)
# =============================================================================

def higher_order_function_demo() -> None:
    """
    고차 함수 - 함수를 인자로 받거나 반환하는 함수.
    
    💡 Java 개발자를 위한 팁:
        Java의 Stream API에서 사용하는 패턴과 유사합니다.
        
        Java:
            list.stream().map(x -> x * 2).collect(...)
            
        Python:
            list(map(lambda x: x * 2, list))
            # 또는 더 Pythonic하게:
            [x * 2 for x in list]
    """
    # 함수를 인자로 받는 함수
    def apply_operation(
        x: int, 
        y: int, 
        operation: Callable[[int, int], int]
    ) -> int:
        """두 숫자에 연산을 적용."""
        return operation(x, y)
    
    result = apply_operation(10, 5, lambda a, b: a + b)
    print(f"apply_operation(10, 5, add): {result}")
    
    result = apply_operation(10, 5, lambda a, b: a * b)
    print(f"apply_operation(10, 5, multiply): {result}")
    
    # 함수를 반환하는 함수 (클로저)
    def make_multiplier(n: int) -> Callable[[int], int]:
        """n을 곱하는 함수를 반환."""
        def multiplier(x: int) -> int:
            return x * n
        return multiplier
    
    double = make_multiplier(2)
    triple = make_multiplier(3)
    
    print(f"\ndouble(5): {double(5)}")
    print(f"triple(5): {triple(5)}")
    
    # 내장 고차 함수: map, filter, reduce
    numbers = [1, 2, 3, 4, 5]
    
    # map - 각 요소에 함수 적용
    squared = list(map(lambda x: x**2, numbers))
    print(f"\nmap(square): {squared}")
    
    # filter - 조건에 맞는 요소만 선택
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"filter(even): {evens}")
    
    # reduce - 누적 연산 (functools)
    total = reduce(lambda acc, x: acc + x, numbers)
    print(f"reduce(sum): {total}")
    
    # ⚠️ Pythonic 방식: Comprehension이 더 선호됨
    print("\n💡 Pythonic 방식 (Comprehension):")
    print(f"  squared: {[x**2 for x in numbers]}")
    print(f"  evens: {[x for x in numbers if x % 2 == 0]}")
    print(f"  sum: {sum(numbers)}")


# =============================================================================
# 3️⃣ 람다 (Lambda)
# =============================================================================

def lambda_demo() -> None:
    """
    람다 - 익명 함수.
    
    💡 Java 개발자를 위한 팁:
        Java의 람다와 유사하지만 문법이 다릅니다.
        
        Java: (x, y) -> x + y
        Python: lambda x, y: x + y
        
        ⚠️ Python 람다는 단일 표현식만 가능합니다!
        여러 문장이 필요하면 일반 함수를 사용하세요.
    """
    # 기본 람다
    add = lambda x, y: x + y
    print(f"add(3, 5): {add(3, 5)}")
    
    # 정렬에 람다 사용 (매우 흔한 패턴)
    users = [
        {"name": "Kim", "age": 30},
        {"name": "Lee", "age": 25},
        {"name": "Park", "age": 35},
    ]
    
    # 나이순 정렬
    sorted_by_age = sorted(users, key=lambda u: u["age"])
    print(f"\n나이순: {sorted_by_age}")
    
    # 이름순 정렬
    sorted_by_name = sorted(users, key=lambda u: u["name"])
    print(f"이름순: {sorted_by_name}")
    
    # 여러 키로 정렬
    items = [("apple", 3), ("banana", 2), ("apple", 1), ("banana", 3)]
    sorted_items = sorted(items, key=lambda x: (x[0], x[1]))
    print(f"\n여러 키 정렬: {sorted_items}")
    
    # 람다의 한계 - 단일 표현식만 가능
    print("\n⚠️ 람다의 한계:")
    print("  - 단일 표현식만 가능 (if문, for문 불가)")
    print("  - 복잡한 로직은 일반 함수로 정의")
    print("  - 재사용할 함수는 이름 있는 함수로 정의")


# =============================================================================
# 4️⃣ 클로저 (Closure)
# =============================================================================

def closure_demo() -> None:
    """
    클로저 - 외부 스코프의 변수를 기억하는 함수.
    
    💡 Java 개발자를 위한 팁:
        Java에서 람다가 effectively final 변수만 캡처할 수 있는 것과 달리,
        Python 클로저는 외부 변수를 자유롭게 참조할 수 있습니다.
        
    💡 Go 개발자를 위한 팁:
        Go의 클로저와 매우 유사합니다.
    """
    def counter_factory() -> Callable[[], int]:
        """호출할 때마다 증가하는 카운터 생성."""
        count = 0  # 자유 변수 (free variable)
        
        def counter() -> int:
            nonlocal count  # 외부 변수 수정 선언
            count += 1
            return count
        
        return counter
    
    counter1 = counter_factory()
    counter2 = counter_factory()
    
    print("독립적인 카운터:")
    print(f"  counter1(): {counter1()}, {counter1()}, {counter1()}")
    print(f"  counter2(): {counter2()}, {counter2()}")
    
    # 클로저의 자유 변수 확인
    print(f"\n클로저의 자유 변수: {counter1.__code__.co_freevars}")
    
    # 실용적인 예: 캐싱 데코레이터
    def memoize(func: Callable[..., Any]) -> Callable[..., Any]:
        """결과를 캐싱하는 데코레이터."""
        cache: dict[tuple[Any, ...], Any] = {}
        
        def wrapper(*args: Any) -> Any:
            if args not in cache:
                cache[args] = func(*args)
                print(f"  계산: {func.__name__}{args}")
            else:
                print(f"  캐시 히트: {func.__name__}{args}")
            return cache[args]
        
        return wrapper
    
    @memoize
    def fibonacci(n: int) -> int:
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)
    
    print("\n메모이제이션 피보나치:")
    result = fibonacci(5)
    print(f"  결과: {result}")


# =============================================================================
# 5️⃣ partial - 함수 부분 적용
# =============================================================================

def partial_demo() -> None:
    """
    partial - 일부 인자를 미리 고정한 새 함수 생성.
    
    💡 Java 개발자를 위한 팁:
        Java에서 람다로 래핑하는 것과 유사합니다.
        
        Java: 
            BiFunction<Integer, Integer, Integer> add = (a, b) -> a + b;
            Function<Integer, Integer> add5 = x -> add.apply(5, x);
            
        Python:
            add5 = partial(add, 5)
    """
    def power(base: int, exponent: int) -> int:
        """거듭제곱 계산."""
        return base ** exponent
    
    # partial로 인자 고정
    square = partial(power, exponent=2)
    cube = partial(power, exponent=3)
    
    print(f"square(5): {square(5)}")
    print(f"cube(5): {cube(5)}")
    
    # 위치 인자 고정
    power_of_2 = partial(power, 2)
    print(f"\npower_of_2(10): {power_of_2(10)}")  # 2^10
    
    # 실용적 예: API 클라이언트
    def make_request(method: str, url: str, data: dict[str, Any] | None = None) -> str:
        """HTTP 요청 시뮬레이션."""
        return f"{method} {url} {data}"
    
    get = partial(make_request, "GET")
    post = partial(make_request, "POST")
    
    print(f"\nget('/users'): {get('/users')}")
    print(f"post('/users', data): {post('/users', {'name': 'Kim'})}")


# =============================================================================
# 6️⃣ 함수형 프로그래밍 패턴
# =============================================================================

def functional_patterns_demo() -> None:
    """
    함수형 프로그래밍 패턴.
    
    💡 Java 개발자를 위한 팁:
        Java의 Stream API와 유사한 패턴이지만,
        Python에서는 Comprehension이 더 선호됩니다.
    """
    # 파이프라인 패턴
    def pipe(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
        """함수들을 파이프라인으로 연결."""
        def pipeline(value: Any) -> Any:
            for func in funcs:
                value = func(value)
            return value
        return pipeline
    
    process = pipe(
        lambda x: x * 2,
        lambda x: x + 10,
        lambda x: x / 2,
    )
    
    print(f"파이프라인 (5 * 2 + 10) / 2 = {process(5)}")
    
    # compose (역순 파이프라인)
    def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
        """함수들을 역순으로 합성."""
        return pipe(*reversed(funcs))
    
    # 함수 데코레이터 체이닝
    def add_prefix(prefix: str) -> Callable[[str], str]:
        return lambda s: f"{prefix}{s}"
    
    def add_suffix(suffix: str) -> Callable[[str], str]:
        return lambda s: f"{s}{suffix}"
    
    format_name = pipe(
        str.strip,
        str.title,
        add_prefix("Mr. "),
        add_suffix("!")
    )
    
    print(f"format_name('  john doe  '): {format_name('  john doe  ')}")


# =============================================================================
# 메인 실행
# =============================================================================

def main() -> None:
    """예제 실행."""
    demos = [
        ("1️⃣ 함수는 객체다", function_as_object_demo),
        ("2️⃣ 고차 함수", higher_order_function_demo),
        ("3️⃣ 람다", lambda_demo),
        ("4️⃣ 클로저", closure_demo),
        ("5️⃣ partial", partial_demo),
        ("6️⃣ 함수형 패턴", functional_patterns_demo),
    ]
    
    for title, demo_func in demos:
        print("=" * 60)
        print(f"📌 {title}")
        print("=" * 60)
        demo_func()
        print()


if __name__ == "__main__":
    main()

