"""
03_is_vs_equals.py - 🟠 is vs == 차이

📌 핵심 개념:
    - == : 값(value) 비교 (equals)
    - is : 객체 동일성(identity) 비교 (같은 메모리 주소)
    
    Python은 작은 정수(-5 ~ 256)와 짧은 문자열을 캐싱합니다.
    이로 인해 is 연산자가 예상과 다르게 동작할 수 있습니다.

🔄 다른 언어 비교:
    - Java: == (primitive 값, 참조 비교), equals() (값 비교)
    - Go: == (값 비교), 포인터 비교는 별도
    - Kotlin: == (equals), === (참조 동일성)
    - Python: == (값 비교), is (참조 동일성)

⚠️ 주의사항:
    - None 비교: 항상 is 사용
    - 숫자/문자열 비교: 항상 == 사용
    - is를 값 비교에 사용하지 마세요!

📚 참고: https://docs.python.org/3/reference/expressions.html#is
"""

from __future__ import annotations


# =============================================================================
# 1️⃣ is vs == 기본 개념
# =============================================================================

def basic_comparison_demo() -> None:
    """
    is와 ==의 기본 차이.
    
    💡 Java 개발자를 위한 팁:
        Java에서 String 비교 시 == vs equals()의 차이와 유사합니다.
        
        Java:
            String a = "hello";
            String b = new String("hello");
            a == b;      // false (참조 비교)
            a.equals(b); // true (값 비교)
            
        Python:
            a = "hello"
            b = "hello"
            a is b  # True (인터닝으로 인해!) - 주의!
            a == b  # True (값 비교)
    """
    # 리스트 비교
    list1 = [1, 2, 3]
    list2 = [1, 2, 3]
    list3 = list1
    
    print("리스트 비교:")
    print(f"  list1 = {list1}")
    print(f"  list2 = {list2}")
    print(f"  list3 = list1")
    print()
    print(f"  list1 == list2: {list1 == list2}")  # True (값이 같음)
    print(f"  list1 is list2: {list1 is list2}")  # False (다른 객체)
    print(f"  list1 is list3: {list1 is list3}")  # True (같은 객체)
    print()
    print(f"  id(list1): {id(list1)}")
    print(f"  id(list2): {id(list2)}")
    print(f"  id(list3): {id(list3)}")


# =============================================================================
# 2️⃣ 정수 캐싱 (Small Integer Caching)
# =============================================================================

def integer_caching_demo() -> None:
    """
    Python의 작은 정수 캐싱.
    
    ⚠️ Python은 -5부터 256까지의 정수를 미리 생성해 재사용합니다!
    이로 인해 is 비교 결과가 예상과 다를 수 있습니다.
    """
    print("정수 캐싱 (-5 ~ 256):")
    
    # 캐시 범위 내
    a = 100
    b = 100
    print(f"  a = 100, b = 100")
    print(f"  a == b: {a == b}")  # True
    print(f"  a is b: {a is b}")  # True (캐싱!)
    print(f"  id(a): {id(a)}, id(b): {id(b)}")
    
    # 캐시 범위 밖
    x = 1000
    y = 1000
    print(f"\n  x = 1000, y = 1000")
    print(f"  x == y: {x == y}")  # True
    print(f"  x is y: {x is y}")  # False 또는 True (구현에 따라)
    print(f"  id(x): {id(x)}, id(y): {id(y)}")
    
    # 음수 캐시 범위
    neg1 = -5
    neg2 = -5
    neg3 = -6
    neg4 = -6
    
    print(f"\n  -5 is -5: {neg1 is neg2}")  # True (캐시 범위)
    print(f"  -6 is -6: {neg3 is neg4}")  # False 또는 True
    
    print("""
    ⚠️ 절대 정수 비교에 is를 사용하지 마세요!
       is의 결과는 구현에 따라 달라질 수 있습니다.
       항상 == 를 사용하세요.
    """)


# =============================================================================
# 3️⃣ 문자열 인터닝 (String Interning)
# =============================================================================

def string_interning_demo() -> None:
    """
    문자열 인터닝.
    
    Python은 짧고 단순한 문자열을 인터닝(재사용)합니다.
    """
    print("문자열 인터닝:")
    
    # 짧은 식별자 스타일 문자열
    s1 = "hello"
    s2 = "hello"
    print(f"  s1 = 'hello', s2 = 'hello'")
    print(f"  s1 == s2: {s1 == s2}")  # True
    print(f"  s1 is s2: {s1 is s2}")  # True (인터닝!)
    
    # 공백이 있는 문자열
    s3 = "hello world"
    s4 = "hello world"
    print(f"\n  s3 = 'hello world', s4 = 'hello world'")
    print(f"  s3 == s4: {s3 == s4}")  # True
    print(f"  s3 is s4: {s3 is s4}")  # 구현에 따라 다름
    
    # 동적으로 생성된 문자열
    s5 = "hello"
    s6 = "hel" + "lo"  # 컴파일 타임에 최적화됨
    s7 = "".join(["h", "e", "l", "l", "o"])  # 런타임 생성
    
    print(f"\n  s5 = 'hello'")
    print(f"  s6 = 'hel' + 'lo'")
    print(f"  s7 = ''.join(['h','e','l','l','o'])")
    print(f"  s5 is s6: {s5 is s6}")  # True (컴파일 최적화)
    print(f"  s5 is s7: {s5 is s7}")  # False 보통
    print(f"  s5 == s7: {s5 == s7}")  # True (항상)


# =============================================================================
# 4️⃣ None 비교 - is 사용
# =============================================================================

def none_comparison_demo() -> None:
    """
    None 비교는 항상 is를 사용.
    
    💡 None은 싱글톤 객체이므로 is가 적절합니다.
    """
    print("None 비교 (항상 is 사용!):")
    
    value = None
    
    # ✅ 올바른 방법
    if value is None:
        print("  ✅ value is None: True")
    
    # ❌ 피해야 할 방법 (동작은 하지만 권장하지 않음)
    if value == None:  # noqa: E711
        print("  ⚠️ value == None: True (권장하지 않음)")
    
    print("""
    💡 왜 is를 사용할까?
    
    1. None은 싱글톤 (단 하나의 인스턴스)
    2. is가 더 빠름 (포인터 비교)
    3. __eq__를 오버라이드한 객체에서 예상치 못한 결과 방지
    4. PEP 8 스타일 가이드 권장
    """)
    
    # __eq__ 오버라이드 예시
    class Weird:
        def __eq__(self, other: object) -> bool:
            return True  # 모든 것과 같다고 응답
    
    weird = Weird()
    print("  __eq__ 오버라이드 객체:")
    print(f"    weird == None: {weird == None}")  # True!
    print(f"    weird is None: {weird is None}")  # False (정확함)


# =============================================================================
# 5️⃣ Boolean과 0/1
# =============================================================================

def boolean_demo() -> None:
    """
    Boolean과 정수의 관계.
    
    Python에서 bool은 int의 서브클래스입니다!
    True == 1, False == 0
    """
    print("Boolean과 정수:")
    
    one = 1
    zero = 0
    print(f"  True == one: {True == one}")   # True
    print(f"  True is one: {True is one}")   # False
    print(f"  False == zero: {False == zero}")  # True
    print(f"  False is zero: {False is zero}")  # False
    
    print(f"\n  isinstance(True, int): {isinstance(True, int)}")  # True!
    
    # 실수하기 쉬운 경우
    def check_value(x: int | bool) -> str:
        if x is True:
            return "Boolean True"
        elif x is False:
            return "Boolean False"
        elif x == 1:
            return "Integer 1"
        elif x == 0:
            return "Integer 0"
        return "Other"
    
    print("\n  타입 구분:")
    print(f"    check_value(True): {check_value(True)}")
    print(f"    check_value(1): {check_value(1)}")
    print(f"    check_value(False): {check_value(False)}")
    print(f"    check_value(0): {check_value(0)}")


# =============================================================================
# 6️⃣ 요약
# =============================================================================

def summary() -> None:
    """
    is vs == 요약.
    """
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                   🟠 is vs == 사용 규칙                        ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║  == (equals)                                                  ║
    ║    - 값이 같은지 비교                                         ║
    ║    - 숫자, 문자열, 컬렉션 비교에 사용                         ║
    ║    - __eq__ 메서드 호출                                       ║
    ║                                                               ║
    ║  is (identity)                                                ║
    ║    - 같은 객체인지 비교 (메모리 주소)                         ║
    ║    - None 비교에만 사용: if x is None                        ║
    ║    - 싱글톤 패턴 객체 비교                                    ║
    ║                                                               ║
    ║  ✅ 올바른 사용:                                               ║
    ║    if x is None:           # None 비교                        ║
    ║    if x is not None:                                          ║
    ║    if a == b:              # 값 비교                          ║
    ║                                                               ║
    ║  ❌ 피해야 할 사용:                                            ║
    ║    if x == None:           # is 사용하세요                    ║
    ║    if num is 100:          # == 사용하세요                    ║
    ║    if s is "hello":        # == 사용하세요                    ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)


# =============================================================================
# 메인 실행
# =============================================================================

def main() -> None:
    """예제 실행."""
    demos = [
        ("1️⃣ 기본 비교", basic_comparison_demo),
        ("2️⃣ 정수 캐싱", integer_caching_demo),
        ("3️⃣ 문자열 인터닝", string_interning_demo),
        ("4️⃣ None 비교", none_comparison_demo),
        ("5️⃣ Boolean", boolean_demo),
        ("6️⃣ 요약", summary),
    ]
    
    print("=" * 60)
    print("🟠 is vs == 차이")
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

