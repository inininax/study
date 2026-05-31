"""
01_mutable_default_args.py - 🔴 가변 기본 인자 함정

📌 핵심 개념:
    Python에서 함수의 기본 인자는 함수 정의 시점에 단 한 번만 평가됩니다.
    가변 객체(list, dict, set)를 기본값으로 사용하면, 모든 호출이 같은 객체를 공유합니다!

🔄 다른 언어 비교:
    - Java: 기본 인자 없음, 오버로딩 사용
    - Go: 기본 인자 없음, 옵션 패턴 사용
    - Kotlin: 기본 인자 있음, 매 호출마다 평가됨!
    - Python: 기본 인자 있음, 정의 시 한 번만 평가 ⚠️

⚠️ 주의사항:
    이것은 Python에서 가장 흔한 버그 원인 중 하나입니다!
    Java/Kotlin에서 온 개발자가 특히 많이 실수합니다.

📚 참고: https://docs.python.org/3/faq/programming.html#why-are-default-values-shared-between-objects
"""

from __future__ import annotations

from typing import Any


# =============================================================================
# 1️⃣ ❌ 잘못된 패턴 - 가변 객체를 기본값으로
# =============================================================================

def wrong_pattern_demo() -> None:
    """
    ❌ 잘못된 패턴: 가변 객체를 기본값으로 사용.
    
    💡 Java 개발자를 위한 팁:
        Java에서는 이런 문제가 없습니다.
        Java는 기본 인자가 없고, 오버로딩을 사용하기 때문입니다.
        
    💡 Kotlin 개발자를 위한 팁:
        Kotlin의 기본 인자는 매 호출마다 평가됩니다!
        
        Kotlin: fun add(item: String, items: MutableList<String> = mutableListOf())
        → 매 호출마다 새 리스트 생성
        
        Python: def add(item, items=[])
        → 모든 호출이 같은 리스트 공유!
    """
    # ❌ 잘못된 함수 정의
    def add_item_wrong(item: str, items: list[str] = []) -> list[str]:
        """아이템을 리스트에 추가 (잘못된 버전)."""
        items.append(item)
        return items
    
    print("❌ 잘못된 패턴 실행:")
    print(f"  add_item_wrong('a'): {add_item_wrong('a')}")
    print(f"  add_item_wrong('b'): {add_item_wrong('b')}")  # ['a', 'b'] 가 됨!
    print(f"  add_item_wrong('c'): {add_item_wrong('c')}")  # ['a', 'b', 'c'] 가 됨!
    
    # 왜 이런 일이 발생하는가?
    print("\n⚠️ 왜 이런 일이?")
    print("  - 기본값 []는 함수 정의 시 한 번만 생성됨")
    print("  - 모든 호출이 같은 리스트 객체를 참조함")
    print(f"  - 기본값 객체 id: {id(add_item_wrong.__defaults__[0])}")


# =============================================================================
# 2️⃣ ✅ 올바른 패턴 - None을 기본값으로
# =============================================================================

def correct_pattern_demo() -> None:
    """
    ✅ 올바른 패턴: None을 기본값으로 사용.
    """
    # ✅ 올바른 함수 정의
    def add_item_correct(item: str, items: list[str] | None = None) -> list[str]:
        """아이템을 리스트에 추가 (올바른 버전)."""
        if items is None:
            items = []  # 매 호출마다 새 리스트 생성
        items.append(item)
        return items
    
    print("✅ 올바른 패턴 실행:")
    print(f"  add_item_correct('a'): {add_item_correct('a')}")
    print(f"  add_item_correct('b'): {add_item_correct('b')}")  # ['b'] - 독립적!
    print(f"  add_item_correct('c'): {add_item_correct('c')}")  # ['c'] - 독립적!
    
    # 기존 리스트에 추가도 가능
    my_list: list[str] = ["existing"]
    result = add_item_correct("new", my_list)
    print(f"\n  기존 리스트 사용: {result}")


# =============================================================================
# 3️⃣ dict에서도 같은 문제
# =============================================================================

def dict_default_demo() -> None:
    """
    dict도 가변 객체이므로 같은 문제 발생.
    """
    # ❌ 잘못된 패턴
    def wrong_config(key: str, value: Any, config: dict[str, Any] = {}) -> dict[str, Any]:
        config[key] = value
        return config
    
    print("❌ dict 기본값 문제:")
    print(f"  wrong_config('a', 1): {wrong_config('a', 1)}")
    print(f"  wrong_config('b', 2): {wrong_config('b', 2)}")  # {'a': 1, 'b': 2}!
    
    # ✅ 올바른 패턴
    def correct_config(
        key: str, 
        value: Any, 
        config: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        if config is None:
            config = {}
        config[key] = value
        return config
    
    print("\n✅ dict 올바른 패턴:")
    print(f"  correct_config('a', 1): {correct_config('a', 1)}")
    print(f"  correct_config('b', 2): {correct_config('b', 2)}")  # {'b': 2} - 독립적!


# =============================================================================
# 4️⃣ 클래스에서의 함정
# =============================================================================

def class_default_demo() -> None:
    """
    클래스 메서드에서도 같은 문제 발생.
    """
    # ❌ 잘못된 클래스
    class WrongShoppingCart:
        def __init__(self, items: list[str] = []) -> None:
            self.items = items
        
        def add(self, item: str) -> None:
            self.items.append(item)
    
    print("❌ 클래스 기본값 문제:")
    cart1 = WrongShoppingCart()
    cart1.add("apple")
    print(f"  cart1.items: {cart1.items}")
    
    cart2 = WrongShoppingCart()
    print(f"  cart2.items (새 객체!): {cart2.items}")  # ['apple']이 이미 있음!
    
    cart2.add("banana")
    print(f"  cart1.items: {cart1.items}")  # ['apple', 'banana']
    print(f"  cart2.items: {cart2.items}")  # 같은 리스트!
    print(f"  cart1.items is cart2.items: {cart1.items is cart2.items}")
    
    # ✅ 올바른 클래스
    class CorrectShoppingCart:
        def __init__(self, items: list[str] | None = None) -> None:
            self.items = items if items is not None else []
        
        def add(self, item: str) -> None:
            self.items.append(item)
    
    print("\n✅ 클래스 올바른 패턴:")
    cart3 = CorrectShoppingCart()
    cart3.add("orange")
    print(f"  cart3.items: {cart3.items}")
    
    cart4 = CorrectShoppingCart()
    print(f"  cart4.items (새 객체): {cart4.items}")  # [] - 독립적!
    print(f"  cart3.items is cart4.items: {cart3.items is cart4.items}")


# =============================================================================
# 5️⃣ 기본값 확인하는 방법
# =============================================================================

def inspect_defaults_demo() -> None:
    """
    함수의 기본값을 확인하는 방법.
    """
    def problematic(items: list[str] = []) -> list[str]:
        items.append("x")
        return items
    
    print("기본값 확인:")
    print(f"  __defaults__: {problematic.__defaults__}")
    
    # 3번 호출
    for i in range(3):
        problematic()
        print(f"  호출 {i+1} 후 __defaults__: {problematic.__defaults__}")
    
    print("\n💡 디버깅 팁:")
    print("  함수의 기본값은 __defaults__ 속성으로 확인 가능")
    print("  가변 객체가 기본값이면 호출할수록 변경됨!")


# =============================================================================
# 6️⃣ 요약 및 규칙
# =============================================================================

def summary() -> None:
    """
    가변 기본 인자 규칙 요약.
    """
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                    🔴 가변 기본 인자 규칙                      ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║  ❌ 하지 마세요:                                               ║
    ║     def func(items=[])                                        ║
    ║     def func(config={})                                       ║
    ║     def func(seen=set())                                      ║
    ║                                                               ║
    ║  ✅ 이렇게 하세요:                                             ║
    ║     def func(items=None):                                     ║
    ║         if items is None:                                     ║
    ║             items = []                                        ║
    ║                                                               ║
    ║  💡 왜?                                                        ║
    ║     기본값은 함수 정의 시 한 번만 평가됩니다.                  ║
    ║     가변 객체를 기본값으로 사용하면 모든 호출이 공유합니다.   ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)


# =============================================================================
# 메인 실행
# =============================================================================

def main() -> None:
    """예제 실행."""
    demos = [
        ("1️⃣ ❌ 잘못된 패턴", wrong_pattern_demo),
        ("2️⃣ ✅ 올바른 패턴", correct_pattern_demo),
        ("3️⃣ dict 기본값", dict_default_demo),
        ("4️⃣ 클래스 기본값", class_default_demo),
        ("5️⃣ 기본값 확인", inspect_defaults_demo),
        ("6️⃣ 요약", summary),
    ]
    
    print("=" * 60)
    print("🔴 가변 기본 인자 함정 (Mutable Default Arguments)")
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

