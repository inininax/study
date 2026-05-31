"""
02_quick_tour.py - Python 핵심 기능 5분 투어

📌 핵심 개념:
    Python만의 강력한 기능들을 빠르게 훑어봅니다.
    - List Comprehension
    - Generator
    - Context Manager (with문)
    - Decorator
    - f-string

🔄 다른 언어 비교:
    - Java: Stream API로 유사한 기능, 하지만 더 verbose
    - Go: 대부분 for문으로 직접 구현 필요
    - Kotlin: 컬렉션 연산자로 유사, 코루틴 지원

⚠️ 주의사항:
    이 기능들은 Python을 "Pythonic"하게 만드는 핵심입니다.
    다른 언어 스타일로 작성하면 동료 Python 개발자가 읽기 어려워합니다.

📚 참고: https://docs.python.org/3/tutorial/
"""

from __future__ import annotations

import contextlib
import time
from functools import wraps
from typing import TYPE_CHECKING, Callable, Iterator

if TYPE_CHECKING:
    from typing import Any


# =============================================================================
# 1️⃣ List/Dict/Set Comprehension - Python의 핵심 문법
# =============================================================================

def comprehension_tour() -> None:
    """
    Comprehension - Python의 대표적인 간결한 문법.
    
    💡 Java 개발자를 위한 팁:
        Java Stream API와 유사하지만 훨씬 간결합니다.
        
        Java:
            List<Integer> squares = IntStream.range(0, 10)
                .map(x -> x * x)
                .boxed()
                .collect(Collectors.toList());
                
        Python:
            squares = [x**2 for x in range(10)]
    """
    # List Comprehension
    squares = [x**2 for x in range(10)]
    print(f"제곱수: {squares}")
    
    # 조건부 필터링
    even_squares = [x**2 for x in range(10) if x % 2 == 0]
    print(f"짝수의 제곱: {even_squares}")
    
    # Dict Comprehension
    word = "hello"
    char_count = {char: word.count(char) for char in set(word)}
    print(f"문자 빈도: {char_count}")
    
    # Set Comprehension
    numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
    unique_squares = {x**2 for x in numbers}
    print(f"고유 제곱수: {unique_squares}")
    
    # 중첩 Comprehension (2D → 1D 평탄화)
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flattened = [num for row in matrix for num in row]
    print(f"평탄화: {flattened}")


# =============================================================================
# 2️⃣ Generator - 메모리 효율적인 반복
# =============================================================================

def generator_tour() -> None:
    """
    Generator - 지연 평가(Lazy Evaluation)로 메모리 절약.
    
    💡 Java 개발자를 위한 팁:
        Java의 Stream과 유사한 개념입니다.
        값을 한 번에 메모리에 올리지 않고 필요할 때 생성합니다.
        
    💡 Go 개발자를 위한 팁:
        Go의 channel을 통한 값 전달과 개념적으로 유사합니다.
    """
    
    # Generator Expression (List Comprehension의 () 버전)
    # 메모리: 값을 한 번에 생성하지 않음
    gen = (x**2 for x in range(1000000))
    print(f"Generator 타입: {type(gen)}")
    print(f"처음 5개: {[next(gen) for _ in range(5)]}")
    
    # Generator Function (yield 사용)
    def fibonacci(n: int) -> Iterator[int]:
        """피보나치 수열 생성기."""
        a, b = 0, 1
        for _ in range(n):
            yield a  # return 대신 yield - 함수 상태 유지
            a, b = b, a + b
    
    print(f"피보나치 10개: {list(fibonacci(10))}")
    
    # 무한 Generator
    def infinite_counter() -> Iterator[int]:
        """무한 카운터 (주의: 반드시 제한 필요!)"""
        n = 0
        while True:
            yield n
            n += 1
    
    counter = infinite_counter()
    first_five = [next(counter) for _ in range(5)]
    print(f"무한 카운터 처음 5개: {first_five}")


# =============================================================================
# 3️⃣ Context Manager (with문) - 리소스 관리
# =============================================================================

def context_manager_tour() -> None:
    """
    Context Manager - 리소스 자동 정리.
    
    💡 Java 개발자를 위한 팁:
        Java의 try-with-resources와 동일한 개념입니다.
        
        Java:
            try (FileInputStream fis = new FileInputStream("file.txt")) {
                // ...
            }
            
        Python:
            with open("file.txt") as f:
                # ...
    
    💡 Go 개발자를 위한 팁:
        Go의 defer와 유사하지만 더 구조화되어 있습니다.
    """
    import tempfile
    import os
    
    # 기본 파일 처리
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("Hello, Python!")
        temp_path = f.name
    # 블록을 벗어나면 자동으로 파일 핸들 닫힘
    
    with open(temp_path) as f:
        content = f.read()
    print(f"파일 내용: {content}")
    
    os.unlink(temp_path)  # 임시 파일 삭제
    
    # 여러 리소스 동시 관리
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode='w', delete=False) as f2:
        f1.write("File 1")
        f2.write("File 2")
        paths = (f1.name, f2.name)
    
    for path in paths:
        os.unlink(path)
    
    # 커스텀 Context Manager (클래스)
    class Timer:
        """실행 시간 측정 Context Manager."""
        
        def __enter__(self) -> "Timer":
            self.start = time.perf_counter()
            return self
        
        def __exit__(self, *args: Any) -> None:
            self.elapsed = time.perf_counter() - self.start
            print(f"⏱️  실행 시간: {self.elapsed:.4f}초")
    
    with Timer():
        # 시간이 걸리는 작업
        total = sum(range(1000000))
    
    # 커스텀 Context Manager (데코레이터)
    @contextlib.contextmanager
    def timer_decorator() -> Iterator[None]:
        """데코레이터로 만든 타이머."""
        start = time.perf_counter()
        yield  # 여기서 with 블록 실행
        elapsed = time.perf_counter() - start
        print(f"⏱️  실행 시간: {elapsed:.4f}초")
    
    with timer_decorator():
        total = sum(range(1000000))


# =============================================================================
# 4️⃣ Decorator - 함수/클래스 기능 확장
# =============================================================================

def decorator_tour() -> None:
    """
    Decorator - 함수나 클래스에 기능을 추가하는 패턴.
    
    💡 Java 개발자를 위한 팁:
        Java의 Annotation과 AOP를 합친 것과 유사합니다.
        Spring의 @Transactional, @Cacheable 등과 비슷한 역할.
        
    💡 Kotlin 개발자를 위한 팁:
        고차 함수를 활용한 함수 래핑과 개념적으로 동일합니다.
    """
    
    # 기본 데코레이터
    def log_call(func: Callable[..., Any]) -> Callable[..., Any]:
        """함수 호출 로깅 데코레이터."""
        @wraps(func)  # 원본 함수 메타데이터 보존
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f"📞 {func.__name__} 호출됨, args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            print(f"📤 {func.__name__} 반환: {result}")
            return result
        return wrapper
    
    @log_call
    def add(a: int, b: int) -> int:
        """두 수를 더합니다."""
        return a + b
    
    result = add(3, 5)
    
    # 인자를 받는 데코레이터
    def retry(max_attempts: int = 3, delay: float = 0.1) -> Callable[..., Any]:
        """실패 시 재시도 데코레이터."""
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                last_exception = None
                for attempt in range(1, max_attempts + 1):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        last_exception = e
                        print(f"⚠️  시도 {attempt}/{max_attempts} 실패: {e}")
                        if attempt < max_attempts:
                            time.sleep(delay)
                raise last_exception  # type: ignore
            return wrapper
        return decorator
    
    @retry(max_attempts=3, delay=0.01)
    def unstable_operation(fail_count: list[int]) -> str:
        """처음 2번은 실패하는 함수."""
        if fail_count[0] < 2:
            fail_count[0] += 1
            raise ValueError("일시적 오류!")
        return "성공!"
    
    print("\n재시도 데코레이터 테스트:")
    try:
        result = unstable_operation([0])
        print(f"최종 결과: {result}")
    except ValueError as e:
        print(f"최종 실패: {e}")


# =============================================================================
# 5️⃣ f-string과 문자열 처리
# =============================================================================

def string_tour() -> None:
    """
    f-string - Python 3.6+의 강력한 문자열 포맷팅.
    
    💡 Java 개발자를 위한 팁:
        String.format()이나 MessageFormat보다 훨씬 간결합니다.
        
        Java: String.format("Hello, %s! You are %d years old.", name, age)
        Python: f"Hello, {name}! You are {age} years old."
        
    💡 Kotlin 개발자를 위한 팁:
        Kotlin의 String Template ($변수)과 유사하지만 더 강력합니다.
    """
    name = "Kim"
    age = 30
    salary = 50000.5
    
    # 기본 f-string
    print(f"이름: {name}, 나이: {age}")
    
    # 표현식 사용
    print(f"내년 나이: {age + 1}")
    print(f"대문자 이름: {name.upper()}")
    
    # 포맷 지정
    print(f"급여: {salary:,.2f}원")  # 천 단위 구분, 소수점 2자리
    print(f"급여: {salary:>15,.2f}원")  # 우측 정렬, 15자리
    
    # 날짜/시간 포맷
    from datetime import datetime
    now = datetime.now()
    print(f"현재 시간: {now:%Y-%m-%d %H:%M:%S}")
    
    # 디버깅용 (Python 3.8+)
    x = 10
    y = 20
    print(f"{x=}, {y=}, {x+y=}")  # 변수명과 값 함께 출력
    
    # 멀티라인 f-string
    user_info = f"""
    =============================
    사용자 정보
    =============================
    이름: {name}
    나이: {age}
    급여: {salary:,.2f}원
    =============================
    """
    print(user_info)


# =============================================================================
# 6️⃣ 언패킹(Unpacking) - Python의 편의 기능
# =============================================================================

def unpacking_tour() -> None:
    """
    Unpacking - 컬렉션의 값을 쉽게 분해.
    
    💡 Java 개발자를 위한 팁:
        Java에는 없는 기능입니다!
        Java에서는 배열 인덱스로 직접 접근해야 합니다.
        
    💡 Kotlin 개발자를 위한 팁:
        Kotlin의 destructuring declaration과 유사합니다.
    """
    # 기본 언패킹
    point = (10, 20, 30)
    x, y, z = point
    print(f"x={x}, y={y}, z={z}")
    
    # * 연산자로 나머지 가져오기
    first, *middle, last = [1, 2, 3, 4, 5]
    print(f"first={first}, middle={middle}, last={last}")
    
    # 딕셔너리 언패킹
    defaults = {"host": "localhost", "port": 8080}
    overrides = {"port": 3000, "debug": True}
    config = {**defaults, **overrides}  # 병합
    print(f"config: {config}")
    
    # 함수 인자 언패킹
    def greet(name: str, age: int, city: str) -> None:
        print(f"{name}({age})님, {city}에서 안녕하세요!")
    
    user = {"name": "Kim", "age": 30, "city": "Seoul"}
    greet(**user)  # dict를 키워드 인자로 전달
    
    args = ("Lee", 25, "Busan")
    greet(*args)  # tuple을 위치 인자로 전달
    
    # 스왑
    a, b = 1, 2
    a, b = b, a
    print(f"스왑 후: a={a}, b={b}")


# =============================================================================
# 메인 실행
# =============================================================================

def main() -> None:
    """예제 실행."""
    tours = [
        ("1️⃣ Comprehension", comprehension_tour),
        ("2️⃣ Generator", generator_tour),
        ("3️⃣ Context Manager", context_manager_tour),
        ("4️⃣ Decorator", decorator_tour),
        ("5️⃣ f-string", string_tour),
        ("6️⃣ Unpacking", unpacking_tour),
    ]
    
    for title, tour_func in tours:
        print("=" * 60)
        print(f"📌 {title}")
        print("=" * 60)
        tour_func()
        print()


if __name__ == "__main__":
    main()

