"""
02_collections_comparison.py - Python 컬렉션 vs Java/Go 컬렉션

📌 핵심 개념:
    Python의 기본 컬렉션(list, dict, set, tuple)은 매우 강력하고 유연합니다.
    Java의 컬렉션 프레임워크보다 간결하게 사용할 수 있습니다.

🔄 다른 언어 비교:
    - Java: ArrayList, HashMap, HashSet - Generic 필수
    - Go: slice, map - 타입 명시 필수
    - Kotlin: listOf, mapOf, setOf - 불변/가변 구분
    - Python: list, dict, set - 동적 타입, 기본 가변

⚠️ 주의사항:
    Python의 list는 Java의 ArrayList와 달리 다양한 타입을 섞어 담을 수 있습니다.
    하지만 타입 힌트를 사용하면 일관성을 유지할 수 있습니다.

📚 참고: https://docs.python.org/3/library/stdtypes.html
"""

from __future__ import annotations

from collections import defaultdict, Counter, OrderedDict, deque
from typing import Any


# =============================================================================
# 1️⃣ List - Java ArrayList / Go slice
# =============================================================================

def list_demo() -> None:
    """
    List 사용법.
    
    💡 Java 개발자를 위한 팁:
        - ArrayList<String> → list[str]
        - list.add() → list.append()
        - list.addAll() → list.extend() 또는 +=
        - list.get(i) → list[i]
        - list.set(i, v) → list[i] = v
        
    💡 Go 개발자를 위한 팁:
        - []string{} → []
        - append(slice, elem) → list.append(elem)
        - slice[1:3] → list[1:3] (거의 동일!)
    """
    # 생성
    numbers: list[int] = [1, 2, 3, 4, 5]
    empty: list[str] = []
    mixed = [1, "two", 3.0, True]  # 타입 혼합 가능 (권장하지 않음)
    
    # 추가
    numbers.append(6)  # 끝에 추가
    numbers.insert(0, 0)  # 특정 위치에 삽입
    numbers.extend([7, 8, 9])  # 여러 개 추가
    
    print(f"numbers: {numbers}")
    
    # 조회
    print(f"첫 번째: {numbers[0]}")
    print(f"마지막: {numbers[-1]}")  # 음수 인덱스!
    print(f"뒤에서 두 번째: {numbers[-2]}")
    
    # 슬라이싱 (Go와 유사)
    print(f"numbers[2:5]: {numbers[2:5]}")  # 인덱스 2, 3, 4
    print(f"numbers[:3]: {numbers[:3]}")  # 처음 3개
    print(f"numbers[7:]: {numbers[7:]}")  # 7번 이후 전부
    print(f"numbers[::2]: {numbers[::2]}")  # 2칸씩 건너뛰기
    print(f"numbers[::-1]: {numbers[::-1]}")  # 역순!
    
    # 삭제
    numbers.remove(5)  # 값으로 삭제
    del numbers[0]  # 인덱스로 삭제
    popped = numbers.pop()  # 마지막 요소 제거 및 반환
    print(f"pop된 값: {popped}, numbers: {numbers}")
    
    # 검색
    print(f"3 in numbers: {3 in numbers}")
    print(f"index of 3: {numbers.index(3)}")
    print(f"count of 3: {numbers.count(3)}")
    
    # 정렬
    unsorted = [3, 1, 4, 1, 5, 9, 2, 6]
    sorted_list = sorted(unsorted)  # 새 리스트 반환
    unsorted.sort()  # 제자리 정렬
    unsorted.sort(reverse=True)  # 역순 정렬
    print(f"정렬 후: {unsorted}")


# =============================================================================
# 2️⃣ Dict - Java HashMap / Go map
# =============================================================================

def dict_demo() -> None:
    """
    Dict 사용법.
    
    💡 Java 개발자를 위한 팁:
        - HashMap<String, Integer> → dict[str, int]
        - map.put(k, v) → dict[k] = v
        - map.get(k) → dict[k] 또는 dict.get(k)
        - map.getOrDefault(k, d) → dict.get(k, d)
        - map.containsKey(k) → k in dict
        - map.keySet() → dict.keys()
        - map.values() → dict.values()
        - map.entrySet() → dict.items()
        
    💡 Go 개발자를 위한 팁:
        - map[string]int{} → {}
        - m[k] = v → dict[k] = v
        - v, ok := m[k] → v = dict.get(k) 또는 try/except
    """
    # 생성
    person: dict[str, Any] = {
        "name": "Kim",
        "age": 30,
        "city": "Seoul"
    }
    empty: dict[str, int] = {}
    
    # 추가/수정
    person["email"] = "kim@example.com"
    person["age"] = 31  # 수정
    
    print(f"person: {person}")
    
    # 조회
    print(f"name: {person['name']}")
    print(f"phone (없음): {person.get('phone', 'N/A')}")  # 기본값 지정
    
    # 삭제
    del person["city"]
    email = person.pop("email")  # 제거 및 반환
    print(f"pop된 email: {email}")
    
    # 순회
    print("\n키 순회:")
    for key in person:
        print(f"  {key}: {person[key]}")
    
    print("\n키-값 순회 (권장):")
    for key, value in person.items():
        print(f"  {key}: {value}")
    
    # 유용한 메서드
    keys = list(person.keys())
    values = list(person.values())
    items = list(person.items())
    print(f"\nkeys: {keys}")
    print(f"values: {values}")
    print(f"items: {items}")
    
    # 병합 (Python 3.9+)
    defaults = {"theme": "dark", "lang": "ko"}
    config = person | defaults  # 병합
    print(f"\n병합: {config}")
    
    # Dict Comprehension
    squares = {x: x**2 for x in range(6)}
    print(f"squares: {squares}")


# =============================================================================
# 3️⃣ Set - Java HashSet
# =============================================================================

def set_demo() -> None:
    """
    Set 사용법.
    
    💡 Java 개발자를 위한 팁:
        - HashSet<Integer> → set[int]
        - set.add() → set.add()
        - set.contains() → elem in set
        - set.addAll() → set.update() 또는 |=
        - set.removeAll() → set.difference_update() 또는 -=
        
    💡 Go 개발자를 위한 팁:
        Go에는 Set이 없어서 map[T]bool로 구현합니다.
        Python의 Set은 내장 타입으로 매우 편리합니다.
    """
    # 생성
    numbers: set[int] = {1, 2, 3, 4, 5}
    empty: set[int] = set()  # {} 는 빈 dict!
    from_list = set([1, 2, 2, 3, 3, 3])  # 중복 제거
    
    print(f"numbers: {numbers}")
    print(f"from_list: {from_list}")
    
    # 추가/삭제
    numbers.add(6)
    numbers.discard(10)  # 없어도 에러 없음
    numbers.remove(6)  # 없으면 KeyError
    
    # 집합 연산 (수학적 집합!)
    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}
    
    print(f"\na: {a}")
    print(f"b: {b}")
    print(f"합집합 (a | b): {a | b}")
    print(f"교집합 (a & b): {a & b}")
    print(f"차집합 (a - b): {a - b}")
    print(f"대칭차집합 (a ^ b): {a ^ b}")  # XOR
    
    # 부분집합 검사
    print(f"\n{1, 2} <= {1, 2, 3}: { {1, 2} <= {1, 2, 3} }")  # 부분집합
    print(f"{1, 2} < {1, 2, 3}: { {1, 2} < {1, 2, 3} }")  # 진부분집합
    
    # Set Comprehension
    even_squares = {x**2 for x in range(10) if x % 2 == 0}
    print(f"\neven_squares: {even_squares}")


# =============================================================================
# 4️⃣ Tuple - 불변 리스트
# =============================================================================

def tuple_demo() -> None:
    """
    Tuple 사용법.
    
    💡 Java 개발자를 위한 팁:
        Java에는 Tuple이 없습니다! (Pair, Triple 라이브러리 사용)
        Python의 Tuple은 불변(immutable) 리스트입니다.
        
    💡 Kotlin 개발자를 위한 팁:
        Kotlin의 Pair, Triple과 유사하지만, 크기 제한이 없습니다.
    """
    # 생성
    point: tuple[int, int] = (10, 20)
    single: tuple[int] = (1,)  # 단일 요소는 콤마 필수!
    empty: tuple[()] = ()
    
    print(f"point: {point}")
    print(f"single: {single}, type: {type(single)}")
    print(f"(1) type: {type((1))}")  # int! 괄호일 뿐
    
    # 조회 (리스트와 동일)
    print(f"point[0]: {point[0]}")
    print(f"point[-1]: {point[-1]}")
    
    # 불변!
    # point[0] = 100  # TypeError!
    
    # 언패킹
    x, y = point
    print(f"x={x}, y={y}")
    
    # Named Tuple (구조체처럼 사용)
    from collections import namedtuple
    
    Point = namedtuple('Point', ['x', 'y'])
    p = Point(10, 20)
    print(f"\nNamedTuple: {p}")
    print(f"p.x: {p.x}, p.y: {p.y}")
    
    # typing.NamedTuple (더 현대적)
    from typing import NamedTuple
    
    class User(NamedTuple):
        name: str
        age: int
        email: str = ""  # 기본값 지원
    
    user = User("Kim", 30)
    print(f"User: {user}")
    print(f"user.name: {user.name}")


# =============================================================================
# 5️⃣ collections 모듈 - 특수 컬렉션
# =============================================================================

def collections_module_demo() -> None:
    """
    collections 모듈의 유용한 컬렉션들.
    
    💡 Java 개발자를 위한 팁:
        Java의 ConcurrentHashMap, LinkedHashMap 등과 유사한
        특수 목적 컬렉션들이 있습니다.
    """
    # defaultdict - 기본값 자동 생성
    print("defaultdict:")
    word_count: defaultdict[str, int] = defaultdict(int)
    for word in "hello world hello python".split():
        word_count[word] += 1  # 키가 없어도 자동 생성!
    print(f"  word_count: {dict(word_count)}")
    
    # 리스트 기본값
    groups: defaultdict[str, list[str]] = defaultdict(list)
    groups["a"].append("apple")
    groups["a"].append("ant")
    groups["b"].append("banana")
    print(f"  groups: {dict(groups)}")
    
    # Counter - 빈도 계산
    print("\nCounter:")
    text = "abracadabra"
    counter = Counter(text)
    print(f"  counter: {counter}")
    print(f"  most_common(3): {counter.most_common(3)}")
    
    # Counter 연산
    c1 = Counter("aab")
    c2 = Counter("abc")
    print(f"  c1 + c2: {c1 + c2}")
    print(f"  c1 - c2: {c1 - c2}")
    
    # deque - 양방향 큐 (스택/큐 구현)
    print("\ndeque:")
    dq: deque[int] = deque([1, 2, 3])
    dq.append(4)  # 오른쪽 추가
    dq.appendleft(0)  # 왼쪽 추가
    print(f"  deque: {dq}")
    print(f"  pop: {dq.pop()}")
    print(f"  popleft: {dq.popleft()}")
    
    # 고정 크기 deque (LRU 캐시 등에 유용)
    limited: deque[int] = deque(maxlen=3)
    for i in range(5):
        limited.append(i)
        print(f"  add {i}: {list(limited)}")


# =============================================================================
# 6️⃣ 컬렉션 성능 비교
# =============================================================================

def performance_comparison() -> None:
    """
    컬렉션별 시간 복잡도.
    
    💡 Java 개발자를 위한 팁:
        Java와 비슷하지만, Python dict는 순서 보장(3.7+)입니다!
    """
    print("시간 복잡도 비교:")
    print("""
    ┌─────────────────┬─────────┬─────────┬─────────┐
    │ 연산            │ list    │ dict    │ set     │
    ├─────────────────┼─────────┼─────────┼─────────┤
    │ 조회 (인덱스)   │ O(1)    │ -       │ -       │
    │ 조회 (키/값)    │ O(n)    │ O(1)*   │ O(1)*   │
    │ 삽입 (끝)       │ O(1)*   │ O(1)*   │ O(1)*   │
    │ 삽입 (중간)     │ O(n)    │ -       │ -       │
    │ 삭제 (끝)       │ O(1)    │ O(1)*   │ O(1)*   │
    │ 삭제 (중간)     │ O(n)    │ -       │ -       │
    │ 검색 (in)       │ O(n)    │ O(1)*   │ O(1)*   │
    └─────────────────┴─────────┴─────────┴─────────┘
    * 평균 케이스, 해시 충돌 시 O(n)
    """)
    
    # 실제 벤치마크
    import timeit
    
    # 리스트에서 검색 vs Set에서 검색
    n = 10000
    test_list = list(range(n))
    test_set = set(range(n))
    
    # 존재하는 요소 검색
    list_time = timeit.timeit(lambda: 9999 in test_list, number=1000)
    set_time = timeit.timeit(lambda: 9999 in test_set, number=1000)
    
    print(f"\n검색 성능 (n={n}, 1000회):")
    print(f"  list: {list_time:.4f}초")
    print(f"  set:  {set_time:.4f}초")
    print(f"  차이: {list_time/set_time:.1f}배 빠름")


# =============================================================================
# 메인 실행
# =============================================================================

def main() -> None:
    """예제 실행."""
    demos = [
        ("1️⃣ List", list_demo),
        ("2️⃣ Dict", dict_demo),
        ("3️⃣ Set", set_demo),
        ("4️⃣ Tuple", tuple_demo),
        ("5️⃣ collections 모듈", collections_module_demo),
        ("6️⃣ 성능 비교", performance_comparison),
    ]
    
    for title, demo_func in demos:
        print("=" * 60)
        print(f"📌 {title}")
        print("=" * 60)
        demo_func()
        print()


if __name__ == "__main__":
    main()

