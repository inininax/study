"""
04_comprehensions.py - List/Dict/Set Comprehension 심화

📌 핵심 개념:
    Comprehension은 Python의 대표적인 간결한 문법입니다.
    반복문과 조건문을 한 줄로 표현할 수 있습니다.

🔄 다른 언어 비교:
    - Java: Stream API (.stream().map().filter().collect())
    - Go: 없음, for문으로 직접 구현
    - Kotlin: 컬렉션 연산자 (map, filter)
    - Python: Comprehension [expr for item in iter if cond]

⚠️ 주의사항:
    Comprehension이 항상 좋은 것은 아닙니다!
    너무 복잡하면 가독성이 떨어지므로 일반 for문을 사용하세요.

📚 참고: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
"""

from __future__ import annotations

from typing import Iterator


# =============================================================================
# 1️⃣ List Comprehension 기초
# =============================================================================

def list_comprehension_basics() -> None:
    """
    List Comprehension 기본 문법.
    
    💡 Java 개발자를 위한 팁:
        Java Stream API와 비교:
        
        Java:
            List<Integer> squares = IntStream.range(0, 10)
                .map(x -> x * x)
                .boxed()
                .collect(Collectors.toList());
                
        Python:
            squares = [x**2 for x in range(10)]
    """
    # 기본 형태: [표현식 for 변수 in 이터러블]
    squares = [x**2 for x in range(10)]
    print(f"제곱수: {squares}")
    
    # 조건 필터링: [표현식 for 변수 in 이터러블 if 조건]
    even_squares = [x**2 for x in range(10) if x % 2 == 0]
    print(f"짝수의 제곱: {even_squares}")
    
    # if-else 표현식 (조건 표현식)
    labels = ["짝수" if x % 2 == 0 else "홀수" for x in range(5)]
    print(f"레이블: {labels}")
    
    # 문자열 처리
    names = ["alice", "bob", "charlie"]
    upper_names = [name.upper() for name in names]
    print(f"대문자: {upper_names}")
    
    # 메서드 체이닝
    cleaned = [name.strip().title() for name in ["  alice ", " BOB", "Charlie  "]]
    print(f"정제된 이름: {cleaned}")


# =============================================================================
# 2️⃣ 중첩 Comprehension
# =============================================================================

def nested_comprehension_demo() -> None:
    """
    중첩 Comprehension.
    
    💡 주의: 
        중첩이 깊어지면 가독성이 떨어집니다.
        2중 중첩까지만 Comprehension으로, 그 이상은 for문으로!
    """
    # 2D → 1D 평탄화 (flatten)
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flattened = [num for row in matrix for num in row]
    print(f"평탄화: {flattened}")
    
    # 위 코드는 다음과 동일:
    # flattened = []
    # for row in matrix:
    #     for num in row:
    #         flattened.append(num)
    
    # 2D 리스트 생성
    rows, cols = 3, 4
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    print(f"\n3x4 그리드: {grid}")
    
    # 구구단
    multiplication_table = [
        [i * j for j in range(1, 10)]
        for i in range(2, 10)
    ]
    print(f"\n구구단 (2~9단):")
    for i, row in enumerate(multiplication_table, start=2):
        print(f"  {i}단: {row}")
    
    # 조건부 중첩
    pairs = [(x, y) for x in range(3) for y in range(3) if x != y]
    print(f"\n(x, y) where x != y: {pairs}")


# =============================================================================
# 3️⃣ Dict Comprehension
# =============================================================================

def dict_comprehension_demo() -> None:
    """
    Dict Comprehension.
    
    💡 Java 개발자를 위한 팁:
        Java Stream의 Collectors.toMap()과 유사합니다.
        
        Java:
            Map<String, Integer> lengths = names.stream()
                .collect(Collectors.toMap(
                    name -> name,
                    name -> name.length()
                ));
                
        Python:
            lengths = {name: len(name) for name in names}
    """
    # 기본 형태
    names = ["alice", "bob", "charlie"]
    name_lengths = {name: len(name) for name in names}
    print(f"이름 길이: {name_lengths}")
    
    # 값 변환
    prices = {"apple": 1000, "banana": 1500, "cherry": 2000}
    discounted = {item: price * 0.9 for item, price in prices.items()}
    print(f"10% 할인: {discounted}")
    
    # 조건 필터링
    expensive = {item: price for item, price in prices.items() if price >= 1500}
    print(f"1500원 이상: {expensive}")
    
    # 키-값 교환
    inverted = {v: k for k, v in prices.items()}
    print(f"키-값 교환: {inverted}")
    
    # 리스트를 딕셔너리로 (enumerate)
    fruits = ["apple", "banana", "cherry"]
    indexed = {i: fruit for i, fruit in enumerate(fruits)}
    print(f"인덱스 딕셔너리: {indexed}")
    
    # 두 리스트를 딕셔너리로 (zip)
    keys = ["name", "age", "city"]
    values = ["Kim", 30, "Seoul"]
    combined = {k: v for k, v in zip(keys, values)}
    # 더 간단히: combined = dict(zip(keys, values))
    print(f"zip 결합: {combined}")


# =============================================================================
# 4️⃣ Set Comprehension
# =============================================================================

def set_comprehension_demo() -> None:
    """
    Set Comprehension.
    
    💡 Go 개발자를 위한 팁:
        Go에는 Set이 없어서 map[T]bool{}로 구현합니다.
        Python은 Set이 내장 타입이고 Comprehension도 지원합니다.
    """
    # 중복 제거
    numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
    unique = {n for n in numbers}
    print(f"중복 제거: {unique}")
    
    # 연산 결과의 고유값
    squares = {x**2 for x in range(-5, 6)}
    print(f"제곱수 (중복 자동 제거): {squares}")
    
    # 문자열에서 고유 문자
    text = "hello world"
    unique_chars = {c for c in text if c != " "}
    print(f"고유 문자: {unique_chars}")
    
    # 조건부 Set
    words = ["apple", "Banana", "CHERRY", "date"]
    starts_with_vowel = {w.lower() for w in words if w[0].lower() in "aeiou"}
    print(f"모음으로 시작: {starts_with_vowel}")


# =============================================================================
# 5️⃣ Generator Expression
# =============================================================================

def generator_expression_demo() -> None:
    """
    Generator Expression - 메모리 효율적인 Comprehension.
    
    💡 핵심 차이:
        - List Comprehension []: 모든 값을 메모리에 저장
        - Generator Expression (): 필요할 때 값 생성 (지연 평가)
    """
    # List Comprehension - 모든 값을 메모리에
    squares_list = [x**2 for x in range(1000)]
    print(f"List: {type(squares_list)}, len={len(squares_list)}")
    
    # Generator Expression - 지연 평가
    squares_gen = (x**2 for x in range(1000))
    print(f"Generator: {type(squares_gen)}")
    
    # Generator는 한 번만 순회 가능
    print(f"처음 5개: {[next(squares_gen) for _ in range(5)]}")
    
    # 큰 데이터에서의 메모리 절약
    import sys
    
    # 리스트: 모든 데이터 저장
    list_size = sys.getsizeof([x**2 for x in range(10000)])
    
    # 제너레이터: 값 저장 안 함
    gen_size = sys.getsizeof(x**2 for x in range(10000))
    
    print(f"\n메모리 비교 (10000개):")
    print(f"  List: {list_size:,} bytes")
    print(f"  Generator: {gen_size:,} bytes")
    print(f"  차이: {list_size / gen_size:.1f}배")
    
    # sum, max, min 등에 직접 사용 (가장 효율적)
    total = sum(x**2 for x in range(1000))  # 괄호 생략 가능
    print(f"\n제곱수 합계: {total}")
    
    # any, all과 함께
    numbers = [1, 2, 3, 4, 5]
    has_even = any(n % 2 == 0 for n in numbers)
    all_positive = all(n > 0 for n in numbers)
    print(f"짝수 존재: {has_even}, 모두 양수: {all_positive}")


# =============================================================================
# 6️⃣ 언제 Comprehension을 사용할까?
# =============================================================================

def when_to_use_comprehension() -> None:
    """
    Comprehension 사용 가이드라인.
    """
    print("✅ Comprehension을 사용할 때:")
    print("  - 간단한 변환/필터링")
    print("  - 한 줄로 읽히는 경우")
    print("  - 부작용(side effect)이 없는 경우")
    
    print("\n❌ for문을 사용할 때:")
    print("  - 복잡한 로직")
    print("  - 여러 줄이 필요한 경우")
    print("  - 부작용이 있는 경우 (I/O, 상태 변경)")
    print("  - 예외 처리가 필요한 경우")
    
    # 좋은 예
    numbers = [1, 2, 3, 4, 5]
    doubled = [n * 2 for n in numbers]
    print(f"\n✅ 좋은 예: {doubled}")
    
    # 나쁜 예 - 부작용이 있음
    print("\n❌ 나쁜 예 (부작용):")
    print("  [print(n) for n in numbers]  # 리스트 생성이 목적이 아님!")
    print("  → for n in numbers: print(n)  # 이렇게!")
    
    # 나쁜 예 - 너무 복잡
    print("\n❌ 나쁜 예 (복잡):")
    complex_example = """
    result = [
        process(item) 
        for sublist in nested 
        for item in sublist 
        if validate(item) and check(item) and filter(item)
    ]
    """
    print(f"  {complex_example}")
    print("  → 일반 for문으로 분리하세요!")
    
    # 가독성 개선 예
    print("\n✅ 가독성을 위한 분리:")
    data = [{"name": "Kim", "active": True}, {"name": "Lee", "active": False}]
    
    # 한 줄보다...
    # active_names = [d["name"].upper() for d in data if d["active"]]
    
    # 여러 줄로 나누어도 됩니다
    active_names = [
        user["name"].upper()
        for user in data
        if user["active"]
    ]
    print(f"  활성 사용자: {active_names}")


# =============================================================================
# 7️⃣ Comprehension 성능
# =============================================================================

def comprehension_performance() -> None:
    """
    Comprehension vs for문 성능 비교.
    """
    import timeit
    
    n = 10000
    
    # List Comprehension
    comp_time = timeit.timeit(
        "[x**2 for x in range(1000)]",
        number=n
    )
    
    # 일반 for문
    loop_code = """
result = []
for x in range(1000):
    result.append(x**2)
"""
    loop_time = timeit.timeit(loop_code, number=n)
    
    # map + lambda
    map_time = timeit.timeit(
        "list(map(lambda x: x**2, range(1000)))",
        number=n
    )
    
    print(f"성능 비교 ({n}회 반복):")
    print(f"  List Comprehension: {comp_time:.3f}초")
    print(f"  for문 + append:     {loop_time:.3f}초")
    print(f"  map + lambda:       {map_time:.3f}초")
    print(f"\n💡 Comprehension이 {loop_time/comp_time:.1f}배 빠름!")
    print("   (내부 최적화 덕분)")


# =============================================================================
# 메인 실행
# =============================================================================

def main() -> None:
    """예제 실행."""
    demos = [
        ("1️⃣ List Comprehension 기초", list_comprehension_basics),
        ("2️⃣ 중첩 Comprehension", nested_comprehension_demo),
        ("3️⃣ Dict Comprehension", dict_comprehension_demo),
        ("4️⃣ Set Comprehension", set_comprehension_demo),
        ("5️⃣ Generator Expression", generator_expression_demo),
        ("6️⃣ 언제 사용할까?", when_to_use_comprehension),
        ("7️⃣ 성능 비교", comprehension_performance),
    ]
    
    for title, demo_func in demos:
        print("=" * 60)
        print(f"📌 {title}")
        print("=" * 60)
        demo_func()
        print()


if __name__ == "__main__":
    main()

